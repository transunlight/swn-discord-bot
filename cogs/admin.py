"""
Extension `cogs.admin`. Defines:
- Admin
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from ._types import SWNBot, SWNContext


@commands.is_owner()
class Admin(commands.Cog):
    """Admin only commands to make the bot dynamic"""

    def __init__(self, bot: SWNBot):
        self.bot: SWNBot = bot

    async def _execute_extension_action(self, action: str, extension: str):
        if action == "load":
            await self.bot.load_extension(extension)
        elif action == "unload":
            await self.bot.unload_extension(extension)
        elif action == "reload":
            await self.bot.reload_extension(extension)

    async def _modify_extensions(self, action: str, ctx: SWNContext, *extensions: str):
        if len(extensions) == 0:
            await ctx.send("No extensions provided!")

        for extension in extensions:
            try:
                await self._execute_extension_action(action, extension)
            except commands.ExtensionError as err:
                await ctx.send(f"{err.__class__.__name__}: {err}")
            else:
                await ctx.send(f"`{extension}` successfully {action}ed!")

    @commands.command(hidden=True)
    async def load(self, ctx: SWNContext, *extensions: str):
        """Loads the given extensions"""
        await self._modify_extensions("load", ctx, *extensions)

    @commands.command(hidden=True)
    async def unload(self, ctx: SWNContext, *extensions: str):
        """Unloads the given extensions"""
        await self._modify_extensions("unload", ctx, *extensions)

    @commands.command(hidden=True)
    async def reload(self, ctx: SWNContext, *extensions: str):
        """Reloads the given extensions"""
        await self._modify_extensions("reload", ctx, *extensions)


async def setup(bot: SWNBot):
    """
    Setup coroutine for extension :module:`cogs.admin`. Has the following effects:
    - Adds cog :class:`Admin` to the bot
    """
    await bot.add_cog(Admin(bot))


async def teardown(bot: SWNBot):
    """
    Teardown coroutine for extension :module:`cogs.admin`. Has the following effects:
    - Removes cog :class:`Admin` to the bot
    """
    await bot.remove_cog("Admin")
