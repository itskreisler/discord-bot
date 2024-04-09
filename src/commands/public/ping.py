import re
from discord import Message, Client
from re import Match

description = (
    "Comando de prueba para verificar que el bot está funcionando correctamente."
)
expreg = re.compile(r"^\?ping")


async def cmd(client: Client, message: Message, match: Match):
    print(match.group())
    await message.channel.send("¡Nyaaa! ¡Pong!")
