import discord
import json
import importlib
import os
import glob
import re
from discord import Message, Client, VoiceClient
from .lib.settings import TOKEN


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

    async def on_ready(self):
        print(f"¡Conectado como {self.user}!")

    async def on_message(self, message: Message):
        print(f"Mensaje recibido: {message.content}")
        if message.author == self.user:
            return
        for command_name, command_module in self.comandos.items():
            expreg = command_module.expreg
            cmd = command_module.cmd
            match = re.match(expreg, message.content)
            if match:
                await cmd(self, message, match)
                break

    def init(self):
        self.comandos = self.cargar_comandos()
        self.run(TOKEN)

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


def run_bot():
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        queues = []
        voice_clients = {}

        @client.event
        async def on_ready():
            print(f"{client.user} esta ahora corriendo!")

        @client.event
        async def on_message(message: Message):
            if message.author == client.user:
                return

            command, *args = message.content.split()

            if command == "?play":
                if not args:
                    await message.channel.send(
                        "Debes incluir la url después del comando."
                    )
                    return
                await play_command(voice_clients, message, args, queues)
            elif command == "?pause":
                await pause_command(voice_clients, message)
            elif command == "?resume":
                await resume_command(voice_clients, message)
            elif command == "?skip":
                await skip_command(voice_clients, message, queues)
            elif command == "?stop":
                await stop_command(voice_clients, message)
            else:
                await message.channel.send("Comando no reconocido")

        client.run(TOKEN)

    except Exception as e:
        print("Ocurrió un error:", e)
