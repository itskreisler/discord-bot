from ...bot import Bot
from discord import Message, Embed
from re import Match
from ...utils.settings import COMMAND_PREFIX
import re

description = "Comando para obtener información del usuario que uso el comando."

expreg = re.compile(rf"^{COMMAND_PREFIX}me(?:@bot)?", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    user = message.author
    miembros_mencionados = message.mentions
    str_joined = ", ".join([m.name for m in miembros_mencionados])
    # agregar usuario a la lista usuarios premium
    for m in miembros_mencionados:
        client.db.add_premium_user(message.guild.id, m.name)

    # hacer un json stringify de user

    embed = Embed(title="Datos", description="Información del usuario")
    embed.add_field(name="autor", value=user)
    embed.add_field(name="miembros mencionados", value=str_joined)

    await message.channel.send(embed=embed)
