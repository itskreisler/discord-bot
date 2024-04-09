from discord import Message, VoiceClient

from ...bot import Bot
import re
from re import Match

description = "Detiene la reproducción de música en el canal de voz actual."
expreg = re.compile(r"^\?stop(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    voice_clients = client.db.voice_clients
    try:
        voice_clients[message.guild.id].stop()
        await voice_clients[message.guild.id].disconnect()
    except Exception as e:
        print(e)
