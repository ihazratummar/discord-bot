# region imports <- This is foldable
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, has_guild_permissions
from config import bot


# endregion


@bot.tree.command(name="kick", description="Kick a member")
@app_commands.checks.has_permissions(administrator=True)
async def kick(
    interaction: discord.Interaction, user: discord.Member, reason: str = " "
):
    await user.kick()
    await interaction.response.send_message(
        f"{user.name} has been kicked by {interaction.user.name}"
    )


@kick.error
async def kick_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        f"This this an admin only command", ephemeral=True
    )


@bot.tree.command(name="ban", description="Ban a member")
@app_commands.checks.has_permissions(administrator=True)
async def ban(
    interaction: discord.Interaction, user: discord.Member, reason: str = " "
):
    await user.ban()
    await interaction.response.send_message(
        f"{user.name} has been banned by {interaction.user.name}"
    )


@ban.error
async def ban_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        f"This this an admin only command", ephemeral=True
    )


# @client.tree.command(name="unban", description="Unban a member")
# @app_commands.checks.has_permissions(administrator=True)
# async def unban(interaction: discord.Interaction, user: discord.User):
#     await user.unban()

#     for ban_entry in banned_users:
#         user = ban_entry.user

#         if user == member:
#             await interaction.guild.unban(user)
#             await interaction.response.send_message(f"{user.name} has been unbanned")
#             return
#         await interaction.response.send_message(f"Could not find {user.name}")


# @unban.error
# async def unban_error(interaction: discord.Interaction, error):
#     await interaction.response.send_message(
#         f"This this an admin only command", ephemeral=True
#     )


@bot.tree.command(name="embed", description="Send an embed")
async def embed(
    interaction: discord.Interaction,
    title: str,
    *,
    message: str,
    thumbnail: str = " ",
    image: str = " ",
    footer: str = " ",
):
    embed = discord.Embed(title=title, description=message, color=0xE8A213)
    await interaction.response.send_message(embed=embed)


@embed.error
async def embed_error(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"This an admin only command", ephemeral=True
    )


@bot.tree.command(name="purge", description="clear messages")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(thinking=True, ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Purged {amount} messages", ephemeral=True)


@purge.error
async def purge_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        f"This an admin only command", ephemeral=True
    )
