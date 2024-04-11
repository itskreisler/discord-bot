import discord
import json
import importlib
import os
import glob
import re
import asyncio
from discord import Message, Client, VoiceClient
from time import sleep
from discord.channel import VoiceChannel, StageChannel
from .utils.settings import TOKEN, ffmpeg_options, SUPER_ADMIN
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from typing import TypedDict, List, Tuple, Union, Callable, Dict


class ResultList(TypedDict):
    link: str
    title: str


class VideosSearchINFO(TypedDict):
    result: List[ResultList]


class YTDLINFO(TypedDict):
    url: str
    title: str


class SEARCHYT(TypedDict):
    source: str
    title: str


class CMD:
    description: str
    expreg: re.Pattern
    cmd: Callable


class DB:
    super_admin: List[str] = SUPER_ADMIN
    premium_users: Dict[int, List[str]] = {}
    """
    {
        1234: ["user123", "user456"],  # Guild ID 1234 has premium users user123 and user456
        5678: ["user789"]  # Guild ID 5678 has premium user user789
    }
    """

    # Add a premium user to a guild
    def add_premium_user(self, guild_id: int, user_id: str) -> None:
        # Check if the guild is already in the list
        if guild_id not in self.premium_users:
            self.premium_users[guild_id] = []  # Create an empty list for new guilds
        # check if the user is already in the list
        if user_id not in self.premium_users[guild_id]:
            self.premium_users[guild_id].append(user_id)
            # Añade el usuario a la lista de premium si no está

    def is_guild_premium_exists(self, guild_id: int) -> bool:
        return guild_id in self.premium_users

    def is_premium_user(self, guild_id: int, user_id: str) -> bool:
        return (
            guild_id in self.premium_users and user_id in self.premium_users[guild_id]
        )


class Bot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: DB = DB()
        self.activity = discord.Game(name="?help")
        # Define la ruta de tu carpeta de comandos
        self.COMANDOS_FOLDER = "commands"
        self.SRC_FOLDER = "src"
        self.comandos: dict[str, CMD]

        # all the music related stuff
        self.is_playing = False
        self.is_paused = False

        self.music_queue: List[Tuple[SEARCHYT, Union[VoiceChannel, StageChannel]]] = []
        """
        .. code-block:: python3
            # [({source,title}, channel)]
        """
        self.YDL_OPTIONS = {
            "format": "bestaudio/best",
            "noplaylist": True,
            # ,"postprocessors": [
            #    {
            #        "key": "FFmpegExtractAudio",
            #        "preferredcodec": "wav",
            #    }
            # ],
            # "outtmpl": f".\%(title)s.%(ext)s",  # this is where you can edit how you'd like the filenames to be formatted
        }
        self.FFMPEG_OPTIONS = ffmpeg_options
        self.vc: VoiceClient = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    async def on_ready(self):
        print(f"Lita de super admins: {self.db.super_admin}")
        print(f"¡Conectado como {self.user}!")
        # asyncio.run_coroutine_threadsafe(self.check_music(), self.loop)

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        print(f"Mensaje recibido: {message.content}")
        existsCommand, command = self.encontrar_comando(message.content)
        if existsCommand:
            expreg, cmd = command
            print(f"Comando encontrado: {expreg}")
            await cmd(self, message, re.match(expreg, message.content))

    def init(self):
        self.comandos = self.cargar_comandos()
        self.run(TOKEN)

    def search_yt(self, item: str) -> dict[str, SEARCHYT]:
        if item.startswith("https://"):
            title: YTDLINFO = self.ytdl.extract_info(item, download=False)
            titulo: str = title["title"]
            return {"source": item, "title": titulo}
        q = VideosSearch(item, limit=1)
        search: VideosSearchINFO = q.result()
        return {
            "source": search["result"][0]["link"],
            "title": search["result"][0]["title"],
        }

    # infinite loop checking
    async def play_music(self, message: Message):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]
            # try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                # in case we fail to connect
                if self.vc == None:
                    await message.channel.send(
                        "```Could not connect to the voice channel```"
                    )
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data: YTDLINFO = await loop.run_in_executor(
                None, lambda: self.ytdl.extract_info(m_url, download=False)
            )
            song = data["url"]
            sleep(2)
            self.vc.play(
                discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS),
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(), self.loop
                ),
            )

        else:
            self.is_playing = False

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]["source"]

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data: YTDLINFO = await loop.run_in_executor(
                None, lambda: self.ytdl.extract_info(m_url, download=False)
            )
            song = data["url"]
            sleep(2)
            self.vc.play(
                discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS),
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(), self.loop
                ),
            )
        else:
            self.is_playing = False

    def encontrar_comando(self, texto):
        for command_name, command_module in self.comandos.items():
            expreg = command_module.expreg
            cmd = command_module.cmd
            match = re.match(expreg, texto)
            if match:
                return True, (expreg, cmd)
        return False, None

    def cargar_comandos(self):
        comandos = {}
        ruta_comandos = os.path.join(
            os.getcwd(), self.SRC_FOLDER, self.COMANDOS_FOLDER, "**", "*.py"
        )
        for command_file in glob.iglob(ruta_comandos, recursive=True):
            module_name = os.path.splitext(os.path.basename(command_file))[0]
            module_path = command_file.replace(os.getcwd(), "").replace(
                os.path.sep, "."
            )[1:][:-3]
            try:
                module: CMD = importlib.import_module(module_path)
                comandos.update({module_name: module})
            except Exception as e:
                print(f"Error al cargar el módulo {module_name}: {e}")
        print("\033[92mComandos cargados exitosamente!\033[0m")
        return comandos

    def get_debug(self):
        db_dict = {
            "super_admin": self.db.super_admin,
            "premium_users": self.db.premium_users,
        }
        atributos = {
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "music_queue": self.music_queue,
            "vc": self.vc,
            "db": db_dict,
            # "ytdl": self.ytdl
        }

        ##print(atributos)
        return atributos

    # validar si el bot no esta reproduciendo musica durante 5 minutos, entonces desconectarlo
    async def check_music(self):
        while True:
            # Check inactivity
            print("Checking inactivity")
            await asyncio.sleep(300)
            # ifNotPP = not any([self.is_playing, self.is_paused])
            # ifCola = len(self.music_queue) == 0
            # print(f"ifNotPP: {ifNotPP}, ifCola: {ifCola}")
            # If not playing, paused, or in a voice channel, disconnect
            if not self.is_playing:
                if self.vc:
                    await self.vc.channel.send("```❌ Desconectado por inactividad```")
                    await self.vc.disconnect()
                    self.vc = None
                    self.music_queue = []
                    self.is_playing = False
                    self.is_paused = False
                    print("Desconectado por inactividad")
