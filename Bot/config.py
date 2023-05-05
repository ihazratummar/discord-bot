#region imports <- This is foldable
from http.client import *
from urllib import *
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands
from client import *
from welcomer import *
from slash_commands import *
from dotenv import load_dotenv
import os
#endregion
# from twitter import *

load_dotenv()
token=os.getenv('DISCORD_TOKEN')


exts = [
    "cogs.ummaroyin",
    "cogs.welcomer"
]

class Ummaroyin(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)
        
    async def setup_hook(self) ->None:
        
        for ext in exts:
            await self.load_extension(ext)
            
        print("Loaded all cogs") 
        
        await self.tree.sync()
        
    async def on_ready(self):
        print("Bot is ready.")
        
if __name__ == "__main__":
    client = Ummaroyin(command_prefix="!", intents=discord.Intents.all()) 
client.run(token)
