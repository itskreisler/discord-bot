import re
from re import Match
from discord import Message
from ...bot import Bot
from ...utils.settings import COMMAND_PREFIX

description = "Clear the queue"
expreg = re.compile(rf"^{COMMAND_PREFIX}c(?:lear)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    if (
        guild_id in client.vc
        and client.vc[guild_id] != None
        and client.is_playing[guild_id]
    ):
        client.vc[guild_id].stop()
        client.music_queues[guild_id] = []
        await message.reply("```Music queue cleared```")
