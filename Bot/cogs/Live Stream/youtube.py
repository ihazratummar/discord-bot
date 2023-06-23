import discord
from discord.ext import commands
import asyncio
import config


class YouTubeNotifier(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.youtube_channel_id = (
            "YOUR_YOUTUBE_CHANNEL_ID"  # Replace with your YouTube channel ID
        )
        self.notification_channel_id = "539422772560920586"  # Replace with the ID of the channel where you want to send notifications
        self.check_interval = 60  # Interval in seconds to check if you are live

        self.live_message = None
        self.check_live_task = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("YouTubeNotifier cog is ready.")
        self.check_live_task = self.bot.loop.create_task(self.check_live())

    async def check_live(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            # Check if you are live on YouTube here (e.g., using YouTube Data API)

            # If you are live, send a notification to the specified channel
            if self.is_live():
                if not self.live_message:
                    channel = self.bot.get_channel(self.notification_channel_id)
                    self.live_message = await channel.send("I am now live on YouTube!")
            # If you are not live anymore, delete the previous notification message
            elif self.live_message:
                await self.live_message.delete()
                self.live_message = None

            await asyncio.sleep(self.check_interval)

    def is_live(self):
        # Implement the logic to check if you are live on YouTube
        # You can use YouTube Data API or any other method to determine your live status
        # Return True if you are live, False otherwise
        return False

    def cog_unload(self):
        if self.check_live_task:
            self.check_live_task.cancel()

        if self.live_message:
            asyncio.create_task(self.live_message.delete())


def setup(bot: commands.bot):
    bot.add_cog(YouTubeNotifier(bot))
