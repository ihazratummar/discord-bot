import discord
from discord.ext import commands
import json
from config import Bot
import mysql.connector
import mysql.connector
import json
from mysql.connector.errors import ProgrammingError
from datetime import datetime, timedelta
from config import db


class Settings(commands.Cog):
    def __init__(self, bot=Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        """Set the log channel for deleted messages."""
        await self.save_log_channel(ctx.guild.id, channel.id)
        await ctx.send(f"Log channel set to {channel.mention}")

    async def save_log_channel(self, guild_id, channel_id):
        try:
            query = """INSERT INTO log_channel (guild_id, channel_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE channel_id = VALUES(channel_id)"""
            data = (guild_id, channel_id)
            cursor = self.bot.db.cursor()
            cursor.execute(query, data)
            db.commit()
            cursor.close()
            return result[0] if result else None
        except mysql.connector.Error as error:
            print("Error:", error)

    async def load_settings(self):
        settings = {}
        try:
            query = """SELECT channel_id FROM log_channel WHERE guild_id = %s"""
            data = (str(self.bot.guild.id),)
            cursor = self.bot.db.cursor()
            await cursor.execute(query, data)
            result = await cursor.fetchone()
            if result:
                settings["log_channel_id"] = result[0]
            cursor.close()
        except mysql.connector.Error as error:
            print("Error:", error)

        return settings


async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))
