"""Types for type checking"""

from discord.ext import commands

from bot import SWNBot

SWNContext = commands.Context[SWNBot]
HelpCommand = commands.HelpCommand
