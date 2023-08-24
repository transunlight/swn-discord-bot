"""
Module contains class:
- SWNBot
"""

from __future__ import annotations

import discord
from discord.ext import commands


def _prefix_callable(bot: SWNBot, msg: discord.Message):
    extras = ["!", "?", ""] if msg.guild is None else bot.prefixes_for(msg.guild.id)
    return commands.when_mentioned_or(*extras)(bot, msg)


class SWNBot(commands.Bot):
    """Stars Without Numbers Bot"""

    prefixes: dict[int, list[str]]

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=_prefix_callable, intents=intents)

    async def on_ready(self):
        """Called when the bot is done preparing the data received from Discord"""
        print(f"We have logged in as {self.user}")

    async def setup_hook(self):
        await super().setup_hook()
        await self.load_prefixes()

    async def load_prefixes(self):
        """Load the prefixes from the database into the bot"""

    def prefixes_for(self, guild_id: int) -> list[str]:
        """Return the list of prefixes for the given guild"""
        return self.prefixes.get(guild_id, ["!"])
