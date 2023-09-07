import discord
from discord.ext import commands
from config import Bot
import json
import mysql.connector
from mysql.connector.errors import ProgrammingError
from config import db


class AutoMod(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
            if isinstance(message.author, discord.Member):
                if (
                    message.author.guild_permissions.administrator
                    or message.author == message.guild.owner
                ):
                    pass
                else:
                    await message.delete()

                    dm_message = "Links not allowed"
                    try:
                        await message.author.send(dm_message)
                    except discord.Forbidden:
                        pass

                    log_channel_id = await self.load_log_channel(message.guild.id)
                    log_channel = self.bot.get_channel(log_channel_id)
                    if log_channel:
                        embed = discord.Embed(
                            title="Invite Link Deleted",
                            description=f"Invite Link Deleted in #{message.channel.name}",
                            color=discord.Color.red(),
                        )
                        embed.add_field(name="Author", value=message.author.mention)
                        embed.add_field(name="Content", value=message.content)
                        await log_channel.send(embed=embed)

    async def load_log_channel(self, guild_id):
        try:
            query = """ SELECT channel_id FROM log_channel WHERE guild_id = %s"""
            data = (str(guild_id),)
            cursor = self.bot.db_connection.cursor()
            cursor.execute(query, data)
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]
        except mysql.connector.Error as error:
            print("error: ", error)
        return None


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoMod(bot))
