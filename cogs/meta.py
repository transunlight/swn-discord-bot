"""
Extension `cogs.meta`. Defines:
- Meta
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from ._types import HelpCommand, SWNBot


class SWNHelpCommand(commands.DefaultHelpCommand):
    """Help command"""

    def __init__(self):
        paginator = commands.Paginator(prefix=None, suffix=None)
        super().__init__(paginator=paginator)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            await destination.send(embed=embed)


class Meta(commands.Cog):
    """Commands for utilities related to the bot itself"""

    def __init__(self, bot: SWNBot):
        self.bot: SWNBot = bot
        self._original_help_command: HelpCommand | None = bot.help_command

        bot.help_command = SWNHelpCommand()
        bot.help_command.cog = self

    async def cog_unload(self):
        self.bot.help_command = self._original_help_command


async def setup(bot: SWNBot):
    """
    Setup coroutine for extension `cogs.meta`. Has the following effects:
    - Adds cog `Meta` to the bot
    """
    await bot.add_cog(Meta(bot))


async def teardown(bot: SWNBot):
    """
    Teardown coroutine for extension `cogs.meta`. Has the following effects:
    - Removes cog `Meta` to the bot
    """
    await bot.remove_cog("Meta")
