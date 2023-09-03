"""Tests for bot.py"""
# pyright: reportPrivateUsage=false

from __future__ import annotations

import pytest

from bot import SWNBot, _prefix_callable


class TestSWNBot:
    _bot: SWNBot

    @pytest.fixture(autouse=True)
    def create_bot(self):
        """Creates a SWNBot instance"""
        self._bot = SWNBot()
        yield
        del self._bot

    def test_prefix_callable(self):
        # TODO: Use a mocked message to create test for _prefix_callable
        ...

    def test_init(self):
        assert self._bot.intents.message_content
        assert self._bot.command_prefix is _prefix_callable

    @pytest.mark.asyncio
    async def test_setup_hook(self):
        await self._bot.setup_hook()
        assert not self._bot.prefixes

    @pytest.mark.asyncio
    async def test_prefixes_for(self):
        # TODO: Create test for SWNBot.prefixes_for
        ...
