"""
Discord Bot
"""

import os
import logging

from dotenv import load_dotenv

import discord
from discord.ext import commands

# TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# LOG
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# CLIENT
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="#", intents=intents, log_handler=handler)


@bot.event
async def on_ready():
    """On Ready"""
    print(f"We have logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    """Hi"""
    await ctx.send("Hello!")


if __name__ == "__main__":
    bot.run(TOKEN)
