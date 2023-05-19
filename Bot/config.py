# region imports <- This is foldable
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# endregion


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

exts = [
    "cogs.mod",
    "cogs.welcomer",
    "cogs.error",
    "cogs.general",
    "cogs.fun_commands",
    "cogs.images",
]


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        for ext in exts:
            await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands(s)")

    async def on_ready(self):
        print("Bot is ready.")


if __name__ == "__main__":
    bot = Bot(command_prefix="!", intents=discord.Intents.all())
    bot.run(token)
