"""Test configuration for cogs tests"""
# pylint: disable=redefined-outer-name, protected-access
# pyright: reportPrivateUsage=false

from __future__ import annotations

import discord
from discord.ext import test as dpytest
import pytest_asyncio

from bot import SWNBot


@pytest_asyncio.fixture  # pyright: ignore
async def bot():
    """Fixture to create appropriate bot"""
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    return SWNBot(intents=intents)


@pytest_asyncio.fixture(name="_bot_setup")  # pyright: ignore
async def bot_setup(bot: SWNBot):
    """Fixture to do appropriate setup"""
    await bot._async_setup_hook()

    dpytest.configure(bot)
    await bot.setup_hook()

    yield bot

    await dpytest.empty_queue()
