import discord
from ...bot import Bot
from discord import Message, Embed
from discord.ui import Button
from re import Match
import re
from ...utils.settings import COMMAND_PREFIX


description = "Comando para mostrar la lista de comandos."
expreg = re.compile(rf"^{COMMAND_PREFIX}h(?:elp)?(?:@bot)?")


async def cmd(client: Bot, message: Message, match: Match):
    comandos = """
`?h[help]` - Muestra todos los comandos disponibles

`?pl[play]` `<query>` - Busca la canción en YouTube y la reproduce en tu canal actual. Continuará reproduciendo la canción actual si estaba pausada 

`?q[queue]` - Muestra la cola de reproducción actual 

`?sk[skip]` - Salta la canción que se está reproduciendo actualmente 

`?c[clear]` - Detiene la música y limpia la cola de reproducción 

`?st[stop]` - Desconecta al bot del canal de voz 

`?pa[pause]` - Pausa la canción que se está reproduciendo actualmente o la reanuda si ya está pausada 

`?res[resume]` - Reanuda la reproducción de la canción actual si está pausada

`?rem[remove]` - Elimina la ultima canción de la cola de reproducción
"""
    # Crear un objeto Embed con la lista de comandos y añade un boton para donar a buymeacoffee

    embed: Embed = Embed(
        title="Lista de comandos", description=comandos, color=discord.Color.blue()
    )
    embed.set_footer(text="Made with ❤️ by Kreisler")
    view = discord.ui.View()
    buymeacoffee = Button(
        style=discord.ButtonStyle.green,
        label="Buy me a coffee",
        url="https://www.buymeacoffee.com/kreisler",
        emoji="☕",
    )
    payme = Button(
        style=discord.ButtonStyle.primary,
        label="Paypal",
        url="https://www.paypal.com/paypalme/itskreisler",
        emoji="💰",
    )
    invite_link = Button(
        style=discord.ButtonStyle.url,
        label="Invite me",
        url="https://discord.com/api/oauth2/authorize?client_id=908871545294835723&permissions=8&scope=bot",
        emoji="🤖",
    )
    view.add_item(buymeacoffee)
    view.add_item(payme)
    view.add_item(invite_link)
    await message.reply(embed=embed, view=view)
