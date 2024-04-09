from discord import Message
import asyncio
import yt_dlp
from ...bot import Bot
from ...utils.next_song import play_next_song
import re
from re import Match

description = "Comando para reproducir música."
expreg = re.compile(r"^\?play(?:@bot)?(?:\s+(.+))?$", re.I | re.M | re.S)


async def cmd(client: Bot, message: Message, match: Match):
    text, *_ = match.groups()
    if text is None:
        await message.channel.send("¡Nyaaa! ¡No puedo reproducir una canción vacía!")
        return
    voice_clients = client.db.voice_clients
    queues = client.db.queues
    try:
        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send(
                "Debes estar en un canal de voz para utilizar este comando."
            )
            return

        voice_channel = message.author.voice.channel
        guild_id = message.guild.id

        if guild_id in voice_clients:
            voice_client = voice_clients[guild_id]
        else:
            voice_client = await voice_channel.connect()
            voice_clients[guild_id] = voice_client
    except Exception as e:
        print(e)

    try:
        url = text

        loop = asyncio.get_event_loop()
        yt_dl_options = {
            "format": "bestaudio/best"
            # ,"postprocessors": [
            #    {
            #        "key": "FFmpegExtractAudio",
            #        "preferredcodec": "wav",
            #    }
            # ],
            # "outtmpl": f".\%(title)s.%(ext)s",  # this is where you can edit how you'd like the filenames to be formatted
        }
        ytdl = yt_dlp.YoutubeDL(yt_dl_options)
        # with yt_dlp.YoutubeDL(yt_dl_options) as ydl:
        #     ydl.download([url])
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=False)
        )

        song = data["url"]
        if song is None:
            await message.channel.send("Debes poner la url de tu canción.")

        queues.append(song)

        ifQueues = len(queues) > 1
        print("isQueues", ifQueues)
        ifNotIsPlaying = not voice_client.is_playing() and len(queues) > 0
        print("ifNotIsPlaying", ifNotIsPlaying)

        if ifQueues:
            await message.channel.send(f"Posición de la cola #{len(queues)}")

        if ifNotIsPlaying:
            await play_next_song(voice_client, queues, message)

    except Exception as e:
        print(e)
