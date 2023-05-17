import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import json


class Welcomer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command()
    async def welcome(self, interaction: discord.Interaction):
        with open("./data.json", "r") as f:
            records = json.load(f)

        records[str(interaction.guild_id)] = str(interaction.channel_id)
        with open("./data.json", "w") as f:
            json.dump(records, f)
        await interaction.response.send_message(
            f"Success! {interaction.channel_id} is your welcome channel."
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcomer(bot))
