import re
from ...bot import Bot
from discord import Message
from re import Match

# optional
premium = False
admin = False

# required
description = (
    "Comando de prueba para verificar que el bot está funcionando correctamente."
)
expreg = re.compile(r"^\?d(?:ebug)?$")


async def cmd(client: Bot, message: Message, match: Match):
    d = client.get_debug()
    # enviar mensaje
    await message.channel.send(f"Debug: {d}")
