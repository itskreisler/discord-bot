import discord
from discord import Message, VoiceClient
from ..lib.settings import ffmpeg_options
import asyncio


async def send_message_with_timeout(txt, message: Message):
    try:
        await asyncio.wait_for(message.channel.send(txt), timeout=10)
    except asyncio.TimeoutError:
        print("Tiempo de espera excedido al enviar el mensaje.")


async def play_next_song(voice_client: VoiceClient, queues: list, message: Message):
    if len(queues) > 0:
        next_song_url = queues.pop(0)
        player = discord.FFmpegOpusAudio(next_song_url, **ffmpeg_options)
        voice_client.play(
            player,
            after=lambda e: asyncio.run(play_next_song(voice_client, queues, message)),
        )
    else:
        await send_message_with_timeout("No hay mas elementos en la cola", message)
