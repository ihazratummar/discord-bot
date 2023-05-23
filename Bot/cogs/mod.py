import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from config import Bot
from datetime import datetime


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

    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: int = None,
        reason: str = None,
    ):
        if duration is None:
            # Ban the member permanently
            await member.ban(reason=reason)
            await interaction.response.send_message(
                f"{member.mention} has been permanently banned."
            )
        else:
            # Calculate the ban duration in seconds
            duration_seconds = duration * 60

            # Ban the member for the specified duration
            await member.ban(reason=reason, delete_message_days=0)
            await interaction.response.send_message(
                f"{member.mention} has been banned for {duration} minutes."
            )

            # Unban the member after the specified duration
            await discord.utils.sleep_until(duration_seconds)
            await member.unban(reason="Ban duration expired.")

    @app_commands.command(name="unban", description="Unban a member")
    @app_commands.checks.has_permissions(administrator=True)
    async def unban(self, interaction: discord.Interaction, member: str):
        banned_users = await interaction.guild.bans()

        for ban_entry in banned_users:
            user = ban_entry.user
            if str(user) == member:
                await interaction.guild.unban(user)
                await interaction.response.send_message(
                    f"{user.mention} has been unbanned."
                )
                return

        await interaction.response.send_message("User not found in the ban list.")

    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(
        self, interaction: discord.Interaction, user: discord.Member, *, reason: str
    ):
        embed = discord.Embed(
            title="User Warning",
            description=f"{user.mention} has been warned by {interaction.user.mention}",
            color=discord.Color.dark_purple(),
        )

        embed.add_field(name="Reason", value=reason)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mute", description="mute a member")
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        if member.Voice is None:
            await interaction.response.send_message(
                "The user is not currently in voice channel"
            )
            return
        voice_state = member.voice
        if voice_state.mute:
            await interaction.response.send_message(
                f"{member.mention} is already muted"
            )
        else:
            await voice_state.edit(mute=True)
            await interaction.response.send_message(f"{member.mention} has been muted")


async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot))
