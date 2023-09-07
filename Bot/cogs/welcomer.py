import discord
from discord.ext import commands
from discord import app_commands
import config
import json
import os


class Welcomer(commands.Cog):
    def __init__(self, bot: config.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            first_role_id = 511215381420048384
            first_role = member.guild.get_role(first_role_id)
            if first_role:
                await member.add_roles(first_role)

            second_role_id = 567387858546065408
            second_role = member.guild.get_role(second_role_id)
            if second_role:
                await member.add_roles(second_role)

        with open("data/welcome.json", "r") as f:
            records = json.load(f)
        try:
            channel_id = records[str(member.guild.id)]
        except KeyError:
            return
        channel = self.bot.get_channel(int(channel_id))
        if not channel:
            return

        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}!",
            description=f"Hi {member.mention}, Welcome to our Discord server! We're excited to have you join our community. Feel free to introduce yourself and get to know each other.",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_image(
            url="https://i.gifer.com/DbRQ.gif"
        )  # Replace with your own image URL if desired

        channel_fields = [
            "📣｜sᴇʀᴠᴇʀ-ʀᴜʟᴇs",
            "🎐｜ᴀʙᴏᴜᴛ-ʜᴀᴢʀᴀᴛ",
        ]

        channels_found = []

        for channel_name in channel_fields:
            channel_field = discord.utils.get(
                member.guild.text_channels, name=channel_name
            )
            if channel_field:
                channels_found.append(channel_field.mention)

        if channels_found:
            embed.add_field(
                name="Important Channels",
                value="\n".join(channels_found),
                inline=True,
            )

        channel_fields = [
            "📌｜sᴛʀᴇᴀᴍ",
            "📌｜sᴏᴄɪᴀʟ",
        ]

        channels_found = []

        for channel_name in channel_fields:
            channel_field = discord.utils.get(
                member.guild.text_channels, name=channel_name
            )
            if channel_field:
                channels_found.append(channel_field.mention)

        if channels_found:
            embed.add_field(
                name="Notification",
                value="\n".join(channels_found),
                inline=True,
            )

        inviter = None
        async for entry in member.guild.audit_logs(limit=1):
            if entry.action == discord.AuditLogAction.invite_create:
                inviter = entry.user
                break

        embed.add_field(
            name="Invited By",
            value=inviter.mention if inviter else "Unknown",
            inline=False,
        )

        await channel.send(content=member.mention, embed=embed)

        role_id = 874718527284727838  # Replace with the actual role ID
        role = member.guild.get_role(role_id)
        if role:
            await member.add_roles(role)

    ## Setup welcome channel
    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def welcome(self, interaction: discord.Interaction):
        with open("data/welcome.json", "r") as f:
            records = json.load(f)

        records[str(interaction.guild_id)] = str(interaction.channel_id)
        with open("data/welcome.json", "w") as f:
            json.dump(records, f)

        await interaction.response.send_message(
            f"Successfully {interaction.channel.mention} is your welcome channel."
        )

    @commands.Cog.listener()
    async def on_boost(self, guild: discord.Guild, booster: discord.Member):
        boost_channel_id = 1123909975522160691
        boost_channel = self.bot.get_channel(boost_channel_id)
        if boost_channel:
            message = (f"Thank you for boosting, {booster.mention}",)
        await boost_channel.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcomer(bot))
