import re
from ...bot import Bot
from discord import Message
from re import Match

description = (
    "Comando de prueba para verificar que el bot está funcionando correctamente."
)
expreg = re.compile(r"^\?ping")


async def cmd(client: Bot, message: Message, match: Match):
    print(match.group())
    await message.channel.send("¡Nyaaa! ¡Pong!")
