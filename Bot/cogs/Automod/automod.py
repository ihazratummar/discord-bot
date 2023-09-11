import discord
from discord.ext import commands
from config import Bot
import json


class AutoMod(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.log_channels = self.load_log_channels()

    def load_log_channels(self):
        try:
            with open("Bot/cogs/Automod/log_channels.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_log_channels(self):
        with open("Bot/cogs/Automod/log_channels.json", "w") as file:
            json.dump(self.log_channels, file, indent=4)

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

                    log_channel_id = self.log_channels.get(str(message.guild.id))
                    log_channel = self.bot.get_channel(log_channel_id)
                    if log_channel:
                        embed = discord.Embed(
                            title="Invite Link Deleted",
                            description=f"Invite Link Deleted in <#{message.channel.id}>",
                            color=discord.Color.red(),
                        )
                        embed.add_field(name="Author", value=message.author.mention)
                        embed.add_field(name="Content", value=message.content)
                        await log_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        """Set the log channel for deleted messages."""
        self.log_channels[str(ctx.guild.id)] = channel.id
        self.save_log_channels()
        await ctx.send(f"Log channel set to {channel.mention}")


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoMod(bot))
