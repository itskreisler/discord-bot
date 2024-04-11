from discord import Message
from ...bot import Bot
import re
from re import Match
from ...utils.settings import COMMAND_PREFIX

description = "Pausa la reproducción de música en el canal de voz actual."
expreg = re.compile(rf"^{COMMAND_PREFIX}pa(?:use)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    if guild_id in client.vc and client.vc[guild_id] and client.is_playing[guild_id]:
        client.is_playing[guild_id] = False
        client.is_paused[guild_id] = True
        client.vc[guild_id].pause()
    elif guild_id in client.vc and client.vc[guild_id] and client.is_paused[guild_id]:
        client.is_paused[guild_id] = False
        client.is_playing[guild_id] = True
        client.vc[guild_id].resume()
