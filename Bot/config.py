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
import asyncio

# endregion


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
db = os.getenv("DB_CONFIG")

host = os.getenv("host")
data = os.getenv("database")
user = os.getenv("username")
passw = os.getenv("password")

exts = [
    "cogs.mod",
    "cogs.error",
    "cogs.general",
    "cogs.fun_commands",
    "cogs.images",
    "cogs.pubg_stats",
    "cogs.games",
    "cogs.welcomer",
    "cogs.global_chat",
    "cogs.Rewards.economy",
    "cogs.Automod.automod",
    "cogs.Automod.settings",
]


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)
        self.db_refresh_interval = 300
        self.db_pool = None
        self.db_connection = None

    async def create_db_pool(self):
        try:
            self.db = mysql.connector.connect(
                host=host,
                database=data,
                user=user,
                password=passw,
                autocommit=True,
                connection_timeout=self.db_refresh_interval,
            )
            print("Connected to the database.")
        except (mysql.connector.Error, asyncpg.PoolError) as e:
            print(f"Failed to create database pool. {e}")

    async def check_db_connection(self):
        if self.db_connection and not self.db_connection.is_connected():
            print("database connection lost. Reconnecting...")
            await self.create_db_connection()

    async def on_ready(self):
        for ext in exts:
            await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
        print("Bot is ready.")
        await self.create_db_pool()

    async def close(self):
        if self.db_connection:
            self.db_connection.close()
            print("Closed db connection.")
        await super().close()

    async def on_disconnect(self):
        print("Disconnected from database")
        await self.check_db_connection()


if __name__ == "__main__":
    bot = Bot(command_prefix=".", intents=discord.Intents.all())
    bot.run(token)
