from src.bot import Bot
from src.lib.settings import COMMAND_PREFIX
import discord

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    instance = Bot(intents=intents)
    instance.init()
