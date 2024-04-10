from discord import Message
from ...bot import Bot
import re
from re import Match

description = "Detiene la reproducción de música en el canal de voz actual."
expreg = re.compile(r"^\?st(?:op)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    if client.vc == None:
        await message.reply("```I'm not in a voice channel```")
        return
    client.is_playing = False
    client.is_paused = False
    await client.vc.disconnect()
    # optional
    client.music_queue = []
    client.vc = None
