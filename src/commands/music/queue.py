from discord import Message
from ...bot import Bot
import re
from re import Match
from ...utils.settings import COMMAND_PREFIX

description = "Comando para ver las canciones en cola."

expreg = re.compile(rf"^{COMMAND_PREFIX}q(?:ueue)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    default_response = "```No music in queue```"
    # if there is a queue, show it
    if guild_id not in client.music_queues:
        await message.reply(default_response)
        return
    retval = ""
    for i in range(0, len(client.music_queues[guild_id])):
        retval += f"#{i+1} -" + client.music_queues[guild_id][i][0]["title"] + "\n"

    if retval != "":
        await message.reply(f"```queue:\n{retval}```")
    else:
        await message.reply(default_response)
