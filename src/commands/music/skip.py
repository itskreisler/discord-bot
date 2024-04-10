from discord import Message
from ...bot import Bot
import re
from re import Match

description = "Salta la canción actual."
expreg = re.compile(r"^\?sk(?:ip)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    if client.vc != None and client.vc:
        client.vc.stop()
        # try to play next in the queue if it exists
        await client.play_music(message)
