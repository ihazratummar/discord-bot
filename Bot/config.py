# region imports <- This is foldable
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from asyncpg.pool import create_pool
import asyncpg
import mysql.connector
import urllib.parse
from mysql.connector.errors import ProgrammingError


# endregion


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
# db = os.getenv("DB_CONFIG")

host = os.getenv("hostname")
data = os.getenv("database")
user = os.getenv("username")
passw = os.getenv("password")
port = os.getenv("port_id")

exts = [
    "cogs.mod",
    "cogs.error",
    "cogs.general",
    "cogs.fun_commands",
    "cogs.images",
]


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

        # async def create_db_pool(self):
        #     try:
        #         self.db = mysql.connector.connect(
        #             host=host, database=data, user=user, password=passw, port=port
        #         )
        #         print("Connected to the database.")
        #     except Exception as e:
        #         print(f"Failed to create database pool. {e}")

    async def on_ready(self):
        for ext in exts:
            await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
        print("Bot is ready.")
        # await self.create_db_pool()


if __name__ == "__main__":
    bot = Bot(command_prefix=".", intents=discord.Intents.all())
    bot.run(token)
