"""Test the Admin cog"""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

from discord.ext import commands
from discord.ext import test as dpytest
import pytest

if TYPE_CHECKING:
    from pytest import FixtureRequest

    from bot import SWNBot

    ExtError = commands.ExtensionError


@pytest.mark.asyncio
class TestAdmin:
    @pytest.fixture(params=["a", "b", "a.b"])
    def extension(self, request: FixtureRequest) -> str:
        """Fixture to inject extension names"""
        return request.param

    @pytest.fixture(params=[commands.ExtensionError, None])
    def ext_error(self, request: FixtureRequest, extension: str) -> None | ExtError:
        """Fixture to inject error or None"""
        return None if request.param is None else request.param(name=extension)

    @pytest.fixture(params=["load", "unload", "reload"])
    def ext_action(self, request: FixtureRequest) -> str:
        """Fixture to inject extension actions"""
        return request.param

    @pytest.fixture
    def ext_message(
        self, extension: str, ext_action: str, ext_error: None | ExtError
    ) -> str:
        """Fixture to compute the correct message when an extension command is called"""
        return (
            f"`{extension}` successfully {ext_action}ed!"
            if ext_error is None
            else f"{ext_error.__class__.__name__}: {ext_error}"
        )

    async def test_extension(
        self,
        _bot_setup: SWNBot,
        extension: str,
        ext_action: str,
        ext_error: None | ExtError,
        ext_message: str,
    ):
        with patch(
            f"tests.cogs.conftest.SWNBot.{ext_action}_extension",
            autospec=True,
            side_effect=ext_error,
        ) as mock_func:
            await dpytest.message(f"!{ext_action} {extension}")
            mock_func.assert_called_once_with(_bot_setup, extension)

        assert dpytest.verify().message().content(ext_message)

    async def test_no_extensions(self, ext_action: str, _bot_setup: SWNBot):
        await dpytest.message(f"!{ext_action} ")
        assert dpytest.verify().message().content("No extensions provided!")
