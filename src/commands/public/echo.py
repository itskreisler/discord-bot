import re
from discord import Message, Client
from re import Match

description = "Comando para repetir un mensaje."
expreg = re.compile(r"^\?echo(?:@bot)?(?:\s+(.+))?$", re.I | re.M | re.S)
# /^\/echo(?:@bot)?(?:\s+(.+))?$/ims


async def cmd(client: Client, message: Message, match: Match):
    text, *_ = match.groups()
    if text is None:
        await message.channel.send("¡Nyaaa! ¡No puedo repetir un mensaje vacío!")
    else:
        await message.channel.send(text)
