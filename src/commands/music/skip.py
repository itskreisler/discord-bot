from discord import Message
from ...bot import Bot
import re
from re import Match
from ...utils.next_song import play_next_song

description = "Salta la canción actual."
expreg = re.compile(r"^\?skip(?:@bot)?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    voice_clients = client.db.voice_clients
    queues = client.db.queues
    print("Canciones en cola:", len(queues))
    try:
        guild_id = message.guild.id
        if guild_id not in voice_clients:
            await message.channel.send("El bot no está en un canal de voz.")
            return

        voice_client = voice_clients[guild_id]

        if len(queues) == 0:
            await message.channel.send("No hay canciones en la cola para saltar.")
            return

        await message.channel.send("Canción saltada.")
        voice_client.stop()

        await play_next_song(client, message, voice_clients)
    except Exception as e:
        print(e)
