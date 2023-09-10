import discord
from discord.ext import commands
from asyncpg import Record
from config import Bot
from discord import app_commands
from config import db
import json
import os


class Level(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.content.startswith(
            self.bot.command_prefix
        ):
            user_id = str(message.author.id)
            query = "SELECT level, xp FROM levels WHERE user_id = $1"
            record: Record = await self.bot.db.fetchrow(query, user_id)
            if record:
                level = record["level"]
                xp = record["xp"]
                xp += 5

                if xp >= 50 and level < 1:
                    level = 1
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level} "
                    )
                elif xp >= 350 and level < 5:
                    level = 5
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level} "
                    )
                elif xp >= 1000 and level < 10:
                    level = 10
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level}"
                    )
                elif xp >= 1500 and level < 15:
                    level = 15
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level}"
                    )
                elif xp >= 2000 and level < 20:
                    level = 20
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level}"
                    )
                elif xp >= 2500 and level < 25:
                    level = 25
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level}"
                    )
                elif xp >= 3000 and level < 30:
                    level = 30
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level}"
                    )
                elif xp >= 3500 and level < 35:
                    level = 35
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level}"
                    )
                elif xp >= 4000 and level < 40:
                    level = 40
                    await message.channel.send(
                        f"{message.author.mention}, you have reached level {level}"
                    )

                query = "UPDATE levels SET level = $1, xp = $2 WHERE user_id = $3"
                await self.bot.db.execute(query, level, xp, user_id)
            else:
                query = "INSERT INTO levels (user_id, level, xp) VALUES ($1, 1, 1)"
                await self.bot.db.execute(query, user_id)

    @app_commands.command()
    async def xp(self, interaction: discord.Interaction):
        """Check your current XP"""
        user_id = str(interaction.user.id)
        query = "SELECT xp FROM levels WHERE user_id = $1"
        record: Record = await self.bot.db.fetchrow(query, user_id)
        if record:
            xp = record["xp"]
            embed = discord.Embed(
                title=" ",
                description=f"Your current XP is <:brawl_gems:1109869226837147698> {xp} xp.",
                color=discord.Color.blurple(),
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title=" ",
                description="You don't have any XP yet. Start chatting to earn XP!",
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def level(self, interaction: discord.Interaction):
        """Check your current level"""
        user_id = str(interaction.user.id)
        query = "SELECT level FROM levels WHERE user_id = $1"
        record: Record = await self.bot.db.fetchrow(query, user_id)
        if record:
            level = record["level"]
            em = discord.Embed(
                title=" ",
                description=f"Your current level is <:blurple:1109870387614990367> {level} level.",
                color=discord.Color.blurple(),
            )
            await interaction.response.send_message(embed=em)
        else:
            em = discord.Embed(
                title=" ",
                description="You don't have a level yet. Start chatting to earn XP!",
                color=discord.Color.blurple(),
            )
            await interaction.response.send_message(embed=em)

    @app_commands.command()
    async def resetxp(self, interaction: discord.Interaction):
        """Reset your XP"""
        user_id = str(interaction.user.id)
        query = "UPDATE levels SET level = 0, xp =0 WHERE user_id = $1"
        await self.bot.db.execute(query, user_id)
        await interaction.response.send_message(
            f"Your XP has been reset.", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Level(bot))
