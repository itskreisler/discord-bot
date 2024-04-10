from discord import Message
from ...bot import Bot
import re
from re import Match

description = "Comando para reproducir música."
expreg = re.compile(r"^\?pl(?:ay)?(?:@bot)?(?:\s+(.+))?$", re.I | re.M | re.S)


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
