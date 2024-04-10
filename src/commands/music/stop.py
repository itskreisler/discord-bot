from discord import Message
from ...bot import Bot
import re
from re import Match

description = "Detiene la reproducción de música en el canal de voz actual."
expreg = re.compile(r"^\?st(?:op)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    client.is_playing = False
    client.is_paused = False
    await client.vc.disconnect()
