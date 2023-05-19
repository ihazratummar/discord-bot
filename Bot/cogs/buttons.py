import discord
from discord.ext import commands
from discord import app_commands
from config import Bot


class Prompt(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error


async def setup(bot: commands.Bot):
    await bot.add_cog(Prompt(bot))
