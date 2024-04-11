from ...bot import Bot
import discord
from discord import Message, Embed
from re import Match
from ...utils.settings import COMMAND_PREFIX
import re

description = "Comando para añadir un usuario o mas usuatios premium."

expreg = re.compile(rf"^{COMMAND_PREFIX}add_p(?:remium)?(?:@bot)?", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    miembros_mencionados = message.mentions
    if not miembros_mencionados:
        await message.channel.send("No se han mencionado usuarios.")
        return
    # agregar usuario a la lista usuarios premium
    for miembro in miembros_mencionados:
        client.db.add_premium_user(message.guild.id, miembro.name)

    counter_premium_users = len(client.db.premium_users[guild_id])
    list_premium_users = "\n".join([user for user in client.db.premium_users[guild_id]])
    embed = Embed(
        title="Lista de usuarios premium de este servidor", color=discord.Color.green()
    )
    embed.add_field(
        name="Cantidad de usuarios premium:", value=counter_premium_users, inline=False
    )
    embed.add_field(name="Miembros Premium:", value=list_premium_users, inline=False)

    await message.channel.send(
        embed=embed,
    )
