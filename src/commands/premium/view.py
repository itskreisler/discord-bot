from ...bot import Bot
import discord
from discord import Message, Embed
from re import Match
from ...utils.settings import COMMAND_PREFIX
import re

description = "Comando ver los usuarios premium de este servidor."

expreg = re.compile(rf"^{COMMAND_PREFIX}p(?:remium)?(?:@bot)?", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    guild_id = message.guild.id
    # agregar usuario a la lista usuarios premium
    if not client.db.is_guild_premium_exists(guild_id):
        await message.channel.send(
            "No hay usuarios premium en este servidor, si quieres ser premium habla con el administrador."
        )
        return
    p_u = client.db.premium_users[guild_id]
    counter_premium_users = len(p_u)
    list_premium_users = "\n".join([user for user in p_u])
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
