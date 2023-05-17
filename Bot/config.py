# region imports <- This is foldable
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# import slash_commands

# import mod_commands
# import welcome


# endregion
# intents = discord.Intents.all()
# bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# cogs = ["cogs.mod", "cogs.welcomes", "cogs.fun"]


#   for cog in cogs:
#       await bot.load_extension(cog)


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.mod")
        print("Moderation cog loaded.")
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands(s)")

    async def on_ready(self):
        print("Bot is ready.")


<<<<<<< HEAD
if __name__ == "__main__":
    bot = Bot(command_prefix="!", intents=discord.Intents.all())
    bot.run(token)
=======
# this is a test command

bot.run(token)
>>>>>>> main
