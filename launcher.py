"""
Script which runs the discord bot
"""

import os
import logging

from dotenv import load_dotenv

from bot import SWNBot


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise RuntimeError("Environment variable 'DISCORD_TOKEN' not set")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

bot = SWNBot()
bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
