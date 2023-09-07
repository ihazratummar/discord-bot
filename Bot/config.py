# region imports <- This is foldable
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from asyncpg.pool import create_pool
import asyncpg
import urllib.parse
import asyncio
from discord import Activity, ActivityType

# endregion

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

exts = [
    "cogs.error",
    "cogs.general",
    "cogs.fun_commands",
    "cogs.images",
    "cogs.games",
    "cogs.welcomer",
    # "cogs.Rewards.economy",
    "cogs.Automod.automod",
    # "cogs.Automod.settings",
]


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def on_ready(self):
        for ext in exts:
            await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
        print("Bot is ready.")

<<<<<<< HEAD
        await self.create_db_connection()

    async def close(self):
        if self.db_connection:
            self.db_connection.close()
            print("Closed db connection.")
        await super().close()

    async def on_disconnect(self):
        print("Disconnected from discord")
        while not self.is_closed():
            try:
                await self.wait_until_ready()
                await self.create_db_connection()
                print("Reconnected to discord and database")
            except Exception as e:
                print(f"Reconnection failed. Error: {e}")
                await asyncio.sleep(60)

    async def on_connect(self):
        print("Connected to discord")

=======
>>>>>>> staging

if __name__ == "__main__":
    bot = Bot(command_prefix=".", intents=discord.Intents.all())
    bot.run(token)
