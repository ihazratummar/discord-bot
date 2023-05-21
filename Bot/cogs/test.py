import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import json
import os


class TestCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        await self.bot.db.execute(
            "INSERT INTO ummaroyin_table VALUES ($1, $2)",
            ctx.guild.id,
            "Hello my name is hazrat",
        )
        return await ctx.send("Done")

    @commands.command()
    async def hi(self, ctx: commands.Context):
        record = await self.bot.db.fetchval(
            "SELECT response FROM ummaroyin_table WHERE guild_id =$1", ctx.guild.id
        )
        if not record:
            return await ctx.send("No record found")
        return await ctx.send(record)

    @commands.command()
    async def sethi(self, ctx: commands.Context, *, text: str):
        record = await self.bot.db.fetchval(
            "SELECT * FROM ummaroyin_table WHERE guild_id =$1", ctx.guild.id
        )
        if not record:
            return await ctx.send("No record found")
        await self.bot.db.execute(
            "UPDATE ummaroyin_table SET response = $1 WHERE guild_id = $2",
            text,
            ctx.guild.id,
        )
        return await ctx.send("Done")


async def setup(bot: commands.Bot):
    await bot.add_cog(TestCog(bot))
