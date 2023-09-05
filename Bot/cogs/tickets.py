import discord
from discord.ext import commands
from discord import app_commands
import config
import json
import os
from discord.ui import Button, button, View


class Tickets(commands.Cog):
    def __init__(self, bot: config.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
