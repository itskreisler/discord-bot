from discord import Message
import yt_dlp
from ...bot import Bot
from ...utils.next_song import play_next_song
import re
from re import Match
import asyncio

description = "Comando para reproducir música."
expreg = re.compile(r"^\?play(?:@bot)?(?:\s+(.+))?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    query, *_ = match.groups()
    try:
        voice_channel = message.author.voice.channel
    except:
        await message.channel.send(
            "```You need to connect to a voice channel first!```"
        )
        return
    if client.is_paused:
        client.vc.resume()
    else:
        song = client.search_yt(query)
        if type(song) == type(True):
            await message.channel.send(
                "```Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.```"
            )
        else:
            if client.is_playing:
                await message.channel.send(
                    f"**#{len(client.music_queue)+2} -'{song['title']}'** added to the queue"
                )
            else:
                await message.channel.send(f"**'{song['title']}'** added to the queue")
            client.music_queue.append([song, voice_channel])
            if client.is_playing == False:
                await client.play_music(message)
