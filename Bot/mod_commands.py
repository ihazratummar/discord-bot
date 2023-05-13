# region imports <- This is foldable

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_guild_permissions
import config
import client
from client import *

# endregion


@client.tree.command(name="admin", description="Admin commands")
@commands.has_permissions(administrator=True)
async def admin(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Admin Commands:\n\n`kick` - kick a member\n`ban` - ban a member\n`unban` - unban a member\n`mute` - mute a member\n`unmute` - unmute a member\n`warn` - warn a member\n`mute` - mute a member\n`unmute` - unmute a member\n`warn` - warn a member\n`kick` - kick a member\n`ban` - ban a member\n`unban` - unban a member\n`mute` - mute a member\n`unmute` - unmute a member\n`warn` - warn a member\n`kick` - kick a member\n`ban` - ban a member\n`unban` - unban a member\n`mute` - mute a member"
    )
