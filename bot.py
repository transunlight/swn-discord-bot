"""
Module contains class:
- SWNBot
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from discord import Intents, Message


extensions = [
    "cogs.admin",
    "cogs.meta",
]


def _prefix_callable(bot: SWNBot, msg: Message):
    extras = ["!", "?", ""] if msg.guild is None else bot.prefixes_for(msg.guild.id)
    return commands.when_mentioned_or(*extras)(bot, msg)


class SWNBot(commands.Bot):
    """Stars Without Numbers Bot"""

    prefixes: dict[int, list[str]]

    def __init__(self, intents: Intents | None = None):
        intents = intents or discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=_prefix_callable, intents=intents)

    async def on_ready(self):
        """Called when the bot is done preparing the data received from Discord"""
        print(f"We have logged in as {self.user}")

    async def setup_hook(self):
        await super().setup_hook()
        await self.load_prefixes()

        for extension in extensions:
            await self.load_extension(extension)

    async def load_prefixes(self):
        """Load the prefixes from the database into the bot"""
        self.prefixes = {}

    def prefixes_for(self, guild_id: int) -> list[str]:
        """Return the list of prefixes for the given guild"""
        return self.prefixes.get(guild_id, ["!"])
