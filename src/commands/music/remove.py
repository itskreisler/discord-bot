from discord import Message
from ...bot import Bot
import re
from re import Match


description = "Removes last song added to queue"
expreg = re.compile(r"^\?rem(?:ove)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    cola = len(client.music_queue)
    if cola == 0:
        await message.reply("```No music in queue```")
        return
    client.music_queue.pop()
    await message.reply("```last song removed```")
