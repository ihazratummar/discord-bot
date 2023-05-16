import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import check
import requests
from client import bot



@bot.tree.command(name="slap", description="slap")
async def slap(interaction: discord.Interaction):
    if interaction.channel.is_nsfw():
        r = requests.get("https://nekos.life/api/v2/img/slap")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res["url"])
        await interaction.response.send_message(embed=em)
    else:
        await interaction.response.send_message(
            "This command is only available in NSFW channels.", ephemeral=True
        )
