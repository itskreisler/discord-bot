from discord import Message
from ...bot import Bot
import re
from re import Match
from ...utils.settings import COMMAND_PREFIX

description = "Comando para reproducir música."
expreg = re.compile(
    rf"^{COMMAND_PREFIX}pl(?:ay)?(?:@bot)?(?:\s+(.+))?", re.I | re.M | re.S
)


async def cmd(client: Bot, message: Message, match: Match):
    query, *_ = match.groups()
    try:
        voice_channel = message.author.voice.channel
    except:
        await message.channel.send(
            "```You need to connect to a voice channel first!```"
        )
        return
    guild_id = message.guild.id

    # Resume playback if paused
    if guild_id in client.is_paused and client.is_paused[guild_id]:
        client.vc[guild_id].resume()
    else:
        song = client.search_yt(query)
        if type(song) == type(True):
            await message.channel.send(
                "```Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.```"
            )
        else:
            # si no hay una cola de música para este servidor, cree una vacía
            if guild_id not in client.music_queues:
                client.music_queues[guild_id] = []

            if guild_id in client.is_playing and client.is_playing[guild_id]:
                await message.channel.send(
                    f"**#{len(client.music_queues[guild_id])+2} -'{song['title']}'** added to the queue"
                )
            else:
                await message.channel.send(f"**'{song['title']}'** added to the queue")
            client.music_queues[guild_id].append([song, voice_channel])
            # iniciar el valor defecto de is_playing
            if guild_id not in client.is_playing:
                client.is_playing[guild_id] = False
            if guild_id in client.is_playing and not client.is_playing[guild_id]:
                await client.play_music(message)
