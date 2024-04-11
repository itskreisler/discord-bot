from discord import Message
from ...bot import Bot
import re
from re import Match
from ...utils.settings import COMMAND_PREFIX

description = "Removes last song added to queue"
expreg = re.compile(rf"^{COMMAND_PREFIX}rem(?:ove)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    default_response = "```No music in queue```"
    if guild_id not in client.music_queues:
        await message.reply(default_response)
        return
    cola = len(client.music_queues[guild_id])
    if cola == 0:
        await message.reply(default_response)
        return
    client.music_queues[guild_id].pop()
    await message.reply("```last song removed```")
