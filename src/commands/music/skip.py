from discord import Message
from ...bot import Bot
import re
from re import Match
from ...utils.settings import COMMAND_PREFIX

description = "Salta la canción actual."
expreg = re.compile(rf"^{COMMAND_PREFIX}sk(?:ip)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    if guild_id in client.vc and client.vc[guild_id] != None and client.vc[guild_id]:
        client.vc[guild_id].stop()
        # try to play next in the queue if it exists
        await client.play_music(message)
