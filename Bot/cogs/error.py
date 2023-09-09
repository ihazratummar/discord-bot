import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import asyncio


class ErrorCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingRole):
            role = interaction.guild.get_role(error.missing_role)
            await interaction.response.send_message(f"Missing role Error: {role.name}")

        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                f"Missing permissions Error: {error}"
            )

        elif isinstance(error, app_commands.CommandOnCooldown):
            retry_after = retry_after = round(error.retry_after)
            await interaction.response.send_message(
                f"Command OnCooldown Error. Try again after{retry_after} seconds."
            )

    ## this error for !command_error
    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"Command not found")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Incorrect arguments entered")

        elif isinstance(error, commands.MissingPermissions):
            perms = ""
            for p in error.missing_permissions:
                perms += f"{p},"

            return await ctx.send(f"You need {perms} to use this command.")

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"Command on cooldown")

        elif isinstance(error, commands.ConversionError):
            return await ctx.send("Invalid Arguments")

        elif isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"Member not found")

        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorCog(bot))
