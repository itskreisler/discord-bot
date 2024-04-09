import discord
from discord import Message
from ...bot import Bot
import re
from re import Match

description = "Reanuda la reproducción de música en el canal de voz actual."
expreg = re.compile(r"^\?resume(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    voice_clients = client.db.voice_clients
    try:
        voice_clients[message.guild.id].resume()
    except Exception as e:
        print(e)
