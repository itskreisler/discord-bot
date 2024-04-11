from ...bot import Bot
from discord import Message, Embed
from re import Match
import re

description = "Comando para obtener información del servidor."
expreg = re.compile(r"^\?info(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    user = client.user
    guild = message.guild
    name = guild.name
    description = guild.description
    owner = guild.owner
    member_count = guild.member_count

    embed = Embed(title=name, description=description)
    embed.add_field(name="Owner", value=owner)
    embed.add_field(name="Member Count", value=member_count)
    embed.add_field(name="Bot", value=user.name)

    await message.channel.send(embed=embed)
