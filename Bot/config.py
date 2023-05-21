# region imports <- This is foldable
import discord
<<<<<<< HEAD
=======
from discord.ext import commands
>>>>>>> temp_branch
from dotenv import load_dotenv
from client import bot
import os
<<<<<<< HEAD
import slash_commands
import mod_commands
import welcome


# endregion
=======
from asyncpg.pool import create_pool
import asyncpg


# endregion

>>>>>>> temp_branch

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
# db = os.getenv("DB_CONFIG")

<<<<<<< HEAD

@bot.event
async def on_ready():
    print("Bot is ready.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)


# this is a test command

bot.run(token)
=======
data = os.getenv("database")
user = os.getenv("username")
passw = os.getenv("password")

exts = [
    "cogs.mod",
    "cogs.welcomer",
    "cogs.error",
    "cogs.general",
    "cogs.fun_commands",
    "cogs.images",
    "cogs.test",
    "cogs.economy",
    "cogs.level",
]


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def create_db_pool(self):
        try:
            self.db = await asyncpg.create_pool(
                database=data, user=user, password=passw
            )
            print("Connected to the database.")
        except Exception as e:
            print(f"Failed to create database pool. {e}")

        for ext in exts:
            await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands(s)")

    async def on_ready(self):
        print("Bot is ready.")
        await self.create_db_pool()


if __name__ == "__main__":
    bot = Bot(command_prefix=".", intents=discord.Intents.all())
    bot.run(token)
>>>>>>> temp_branch
