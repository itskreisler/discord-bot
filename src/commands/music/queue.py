from discord import Message
from ...bot import Bot
import re
from re import Match

description = "Comando para ver las canciones en cola."

expreg = re.compile(r"^\?q(?:ueue)?(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    retval = ""
    for i in range(0, len(client.music_queue)):
        retval += f"#{i+1} -" + client.music_queue[i][0]["title"] + "\n"

    if retval != "":
        await message.reply(f"```queue:\n{retval}```")
    else:
        await message.reply("```No music in queue```")
