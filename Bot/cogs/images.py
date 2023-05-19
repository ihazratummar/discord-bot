import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import requests
import asyncpraw
import random


class Images(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="art", description="get a random art")
    async def art(self, interaction: discord.Interaction):
        try:
            subreddits = ["Art", "ArtHistory"]  # Add the desired subreddits here
            subreddit = subreddits[random.randint(0, len(subreddits) - 1)]
            response = requests.get(
                f"https://api.reddit.com/r/{subreddit}/random",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            data = response.json()
            art_url = data[0]["data"]["children"][0]["data"]["url"]
            art_title = data[0]["data"]["children"][0]["data"]["title"]
            embed = discord.Embed(title=art_title, color=discord.Color.random())
            embed.set_image(url=art_url)

            await interaction.response.send_message(
                f"{subreddit}",
                embed=embed,
            )
        except Exception as e:
            print(f"Error retrieving art: {e}")
            await interaction.response.send_message("sorry, i couldn't find")


async def setup(bot: commands.Bot):
    await bot.add_cog(Images(bot))
