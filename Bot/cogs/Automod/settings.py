import discord
from discord.ext import commands
import json
from config import Bot
from datetime import datetime, timedelta


class Settings(commands.Cog):
    def __init__(self, bot=Bot):
        self.bot = bot
        self.settings = self.load_settings()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        """Set the log channel for deleted messages."""
        self.settings[ctx.guild.id] = {"log_channel_id": channel.id}
        self.save_settings()
        await ctx.send(f"Log channel set to {channel.mention}")
        
    def save_settings(self):
        with open("Bot/cogs/Automod/settings.json", "w") as file:
            json.dump(self.settings, file, indent= 4)
    
    def load_settings(self):
        try:
            with open("Bot/cogs/Automod/settings.json", "r") as file:
                return(file)
        except FileNotFoundError:
            return {}
        
    def get_log_channel_id(self, guild_id):
        return self.settings.get(guild_id, {}).get("log_chanel_id")

async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))
