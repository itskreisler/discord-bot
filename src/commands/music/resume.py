from discord import Message
from ...bot import Bot
import re
from re import Match

description = "Reanuda la reproducción de música en el canal de voz actual."
expreg = re.compile(r"^\?res(?:ume)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    if client.is_paused:
        client.is_paused = False
        client.is_playing = True
        client.vc.resume()
