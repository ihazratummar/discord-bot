import discord
from config import Bot
from discord.ext import commands


source_channel_id = 286753650276171787
destination_channel_id = 1122196678494146581


class GlobalChat(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == source_channel_id:
            destination_channel = self.bot.get_channel(destination_channel_id)
            if destination_channel:
                await destination_channel.send(
                    f"{message.author.mention}: {message.content}"
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalChat(bot))
