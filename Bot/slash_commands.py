# region imports <- This is foldable
from urllib import request
import requests
import random
import discord
from discord.ext import commands
from discord.ext.commands import check
from discord.ext.commands import has_permissions
from discord import app_commands
from client import bot
import json
import os

# endregion


@bot.tree.command(name="ping", description="Check your ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")


@bot.tree.command(name="quota", description="Display quota")
async def quota(interaction: discord.Interaction):
    responses = requests.get("https://api.quotable.io/random")
    data = responses.json()
    quota = data["content"]
    author = data["author"]
    await interaction.response.send_message(f"{author}:\n\n━━━━{quota}")


@bot.tree.command(name="wiki", description="Search wikipedia")
async def wiki(interaction: discord.Interaction, query: str):
    import wikipedia

    wikipedia.set_lang("en")
    result = wikipedia.summary(query, sentences=2)
    await interaction.response.send_message(result)


@bot.tree.command(name="pc", description="Check my Gaming and Streaming pc Config")
async def pc(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Gaming PC\n\nCPU:- Ryzen 7 3700x.\nGraphics Card:- 2060 super 8gb.\nMemory - XPG 16GB 3600MHz\nStorage - 1 TB SSD /1TB HDD\n\nStreaming PC\n\nCPU: Intel i3 7th gen\nGPU: 1050Ti 4GB OC\nRAM: 8 GB 2400 MHz\nStorage: 250 GB SSD\nElgato HD60s 14000\nTotal Price:-124500"
    )


@bot.tree.command(
    name="whatsapp", description="whatsapp  group daily stream notification"
)
async def whatsapp(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Join Whatsapp Group for stream notification : https://bit.ly/3zBxoCf"
    )


@bot.tree.command(name="support")
async def support(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"You can support us by becoming a facebook page member.\nBecome a supporter:-  https://bit.ly/3xJdNzZ"
    )


@bot.tree.command(name="social")
async def social(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"You can check all my social profile here :\nhttps://wlo.link/@crazyforsurprise"
    )


@bot.tree.command(name="meme", description="Get random meme")
async def meme(interaction: discord.Interaction):
    try:
        subreddits = [
            "memes",
            "dankmemes",
            "AdviceAnimals",
            "MemeEconomy",
            "terriblefacebookmemes",
        ]  # Add the desired subreddits here
        subreddit = subreddits[random.randint(0, len(subreddits) - 1)]
        response = requests.get(
            f"https://api.reddit.com/r/{subreddit}/random",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        data = response.json()
        meme_url = data[0]["data"]["children"][0]["data"]["url"]
        meme_title = data[0]["data"]["children"][0]["data"]["title"]
        embed = discord.Embed(title=meme_title, color=discord.Color.random())
        embed.set_image(url=meme_url)

        await interaction.response.send_message(
            f"{subreddit}",
            embed=embed,
        )
    except Exception as e:
        print(f"Error retrieving meme: {e}")
        await interaction.response.send_message("sorry, i couldn't find")


@bot.tree.command(name="youtube", description="search video")
async def youtube(interaction: discord.Interaction, search: str):
    response = requests.get(f"https://youtube.com/results?search_query={search}")
    html = response.text
    index = html.find("/watch?v=")
    url = "https://www.youtube.com" + html[index : index + 20]
    await interaction.response.send_message(url)


@bot.tree.command(name="warn", description="Warn a member")
async def warn(interaction: discord.Interaction, user: discord.Member, *, reason: str):
    embed = discord.Embed(
        title="User Warning",
        description=f"{user.mention} has been warned by {interaction.user.mention}",
        color=discord.Color.dark_purple(),
    )

    embed.add_field(name="Reason", value=reason)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="imgur", description="search for images")
async def imgur(interaction: discord.Interaction, *, query: str):
    headers = {"Authorization": "Client-ID 20c2904655c6a1f"}
    params = {"q": query}
    response = requests.get(
        "https://api.imgur.com/3/gallery/search/", headers=headers, params=params
    )

    if response.status_code == 200:
        data = json.loads(response.content.decode("utf-8"))
        images = [item for item in data["data"] if "images" in item and item["images"]]

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


@bot.tree.command(name="invite", description="Invite Link")
async def invite(interaction: discord.Interaction):
    link = await interaction.channel.create_invite(max_age=0)
    await interaction.response.send_message(link)
