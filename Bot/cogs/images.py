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

            if isinstance(data, list) and len(data) > 0:
                art_data = data[0].get("data", {})
                art_url = art_data.get("url")
                art_title = art_data.get("title")

            elif isinstance(data, dict):
                children = data.get("data", {}).get("children", [])
                if children:
                    art_data = children[0]["data"]
                    art_url = art_data.get("url")
                    art_title = art_data.get("title")
                else:
                    art_url = None
            else:
                art_url = None

            if art_url:
                embed = discord.Embed(title=art_title, color=discord.Color.random())
                embed.set_image(url=art_url)
                await interaction.response.send_message(
                    f"From subreddit: {subreddit}", embed=embed
                )
            else:
                await interaction.response.send_message(
                    "Sorry, I couldn't find any art."
                )
        except Exception as e:
            print(f"Error retrieving art: {e}")
            await interaction.response.send_message("Sorry, I couldn't find art.")

    @app_commands.command(name="imgur", description="search for images")
    async def imgur(self, interaction: discord.Interaction, *, query: str):
        headers = {"Authorization": "Client-ID 20c2904655c6a1f"}
        params = {"q": query}
        response = requests.get(
            "https://api.imgur.com/3/gallery/search/", headers=headers, params=params
        )

        if response.status_code == 200:
            data = json.loads(response.content.decode("utf-8"))
            images = [
                item for item in data["data"] if "images" in item and item["images"]
            ]

            if images:
                random_image = random.choice(images)
                image_url = random.choice(random_image["images"])["link"]

                embed = discord.Embed(
                    title=f'Results for "{query}"', color=discord.Color.blue()
                )
                embed.set_image(url=image_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    f'Sorry, no images found for "{query}"'
                )
        else:
            await interaction.response.send_message(
                "Sorry, there was an error processing your request. Please try again later."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Images(bot))
