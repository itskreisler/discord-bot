import discord
from discord import Message
from discord import VoiceClient
from ...bot import Bot
import re
from re import Match

description = "Comando para ver las canciones en cola."

expreg = re.compile(r"^\?queue(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    queues = client.db.queues
    if len(queues) == 0:
        await message.channel.send("No hay canciones en la cola.")
        return
    await message.channel.send("Canciones en cola:")
    for i, song in enumerate(queues):
        await message.channel.send(f"{i + 1}. {song}")
