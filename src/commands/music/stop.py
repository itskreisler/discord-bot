from discord import Message
from ...bot import Bot
import re
from re import Match
from ...utils.settings import COMMAND_PREFIX

description = "Detiene la reproducción de música en el canal de voz actual."
expreg = re.compile(rf"^{COMMAND_PREFIX}st(?:op)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    if guild_id in client.vc and client.vc[guild_id]:
        client.is_playing[guild_id] = False
        client.is_paused[guild_id] = False
        await client.vc[guild_id].disconnect()
        client.music_queues.pop(guild_id, None)  # Remove the music queue for the guild
        client.vc.pop(guild_id, None)  # Remove the VoiceClient for the guild
    else:
        await message.reply("```I'm not in a voice channel```")
