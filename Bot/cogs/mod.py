import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from config import Bot


class Mod(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="timeout", description="timeout a member")
    @app_commands.checks.has_permissions(administrator=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: str = " ",
    ):
        delta = timedelta(minutes=minutes)
        await member.timeout(delta, reason=reason)
        await interaction.response.send_message(
            f"{member.mention} has been timed out for '{reason}'."
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot))
