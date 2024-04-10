import discord
import json
import importlib
import os
import glob
import re
from discord import Message, Client, VoiceClient
from .utils.settings import TOKEN
import asyncio


class CMD:
    description: str
    expreg: re.Pattern
    cmd: callable


class DB(dict):
    queues: list[str] = []
    voice_clients: dict[str, VoiceClient] = {}


class Bot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: DB = DB()
        # Define la ruta de tu carpeta de comandos
        self.COMANDOS_FOLDER = "commands"
        self.SRC_FOLDER = "src"
        self.comandos: dict[str, CMD]
        self.vc = None
        # all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []

    async def on_ready(self):
        print(f"¡Conectado como {self.user}!")

    async def on_message(self, message: Message):
        print(f"Mensaje recibido: {message.content}")
        if message.author == self.user:
            return
        existsCommand, command = self.encontrar_comando(message.content)
        if existsCommand:
            print(f"Comando encontrado: {command}")
            expreg, cmd = command
            await cmd(self, message, re.match(expreg, message.content))

    def init(self):
        self.comandos = self.cargar_comandos()
        self.run(TOKEN)

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
