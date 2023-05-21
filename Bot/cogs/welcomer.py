import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import json
import os


class Welcomer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    ### setup welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
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
            title=f"Welcome {member.name}!",
            description=f"Welcome to the {member.guild.name}! Enjoy your stay here!",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_image(
            url="https://media.discordapp.net/attachments/984308077333454862/1029577248346488852/chat-rules.png?width=1025&height=302"
        )  # Replace with your own image URL if desired

        channel_field = discord.utils.get(
            member.guild.text_channels, name="⤓public-chat👨"
        )
        embed.add_field(
            name="Important Channel", value=channel_field.mention, inline=True
        )
        embed.add_field(name="Invited By", value="invited_by", inline=True)

        await channel.send(content=member.mention, embed=embed)

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


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcomer(bot))
