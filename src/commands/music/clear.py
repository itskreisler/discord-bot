import re
from re import Match
from discord import Message
from ...bot import Bot


description = "Clear the queue"
expreg = re.compile(r"^\?c(?:lear)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):

    if client.vc != None and client.is_playing:
        client.vc.stop()
        client.music_queue = []
        await message.reply("```Music queue cleared```")
