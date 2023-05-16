# region imports <- This is foldable
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from client import bot
import os
import slash_commands
import mod_commands
import welcome
import nsfw_commands


# endregion

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print("Bot is ready.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)


bot.run(token)
