import discord
from discord import Message, VoiceClient
from discord.player import FFmpegOpusAudio
from settings import ffmpeg_options
from ..bot import Bot


async def play_next_song(client: Bot, message: Message, voice_client: VoiceClient):
    queues = client.db.queues
    print("Elementos en la cola:", len(queues))
    if len(queues) > 0:
        # print color azul
        print("\033[94m", "Reproduciendo siguiente canción", "\033[0m")
        try:
            next_song_url = queues.pop(0)
            player = discord.FFmpegOpusAudio(next_song_url, **ffmpeg_options)
            voice_client.play(
                player,
                after=lambda e: _play_next_song(client, message, voice_client),
            )
        except Exception as e:
            print("Error al reproducir la siguiente canción")
    else:
        await message.channel.send("No hay más canciones en la cola.")


async def _play_next_song(client: Bot, message: Message, voice_client: VoiceClient):
    queues = client.db.queues
    next_song_url = queues.pop(0)
    player = discord.FFmpegOpusAudio(next_song_url, **ffmpeg_options)
    voice_client.play(
        player,
        after=lambda e: play_next_song(client, message, voice_client),
    )
