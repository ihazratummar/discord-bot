import discord
from discord.ext import commands
from asyncpg import Record
from config import Bot
from discord import app_commands
from typing import Dict
import mysql.connector
import json
from mysql.connector.errors import ProgrammingError
from datetime import datetime, timedelta


class Economy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.currency_icon = "💵"

    async def get_user_balance(self, user_id: int):
        query = "SELECT balance FROM economy WHERE user_id = %s"
        values = (user_id,)
        cursor = self.bot.db_connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    async def update_user_balance(self, user_id: int, balance: int):
        query = "INSERT INTO economy (user_id, balance) VALUES (%s, %s) ON DUPLICATE KEY UPDATE balance = %s"
        values = (user_id, balance, balance)
        cursor = self.bot.db.cursor()
        cursor.execute(query, values)
        self.bot.db.commit()
        cursor.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.bot and not message.content.startswith(
            self.bot.command_prefix
        ):
            user_id = message.author.id
            user_balance = await self.get_user_balance(user_id)

            special_role_id_1 = 874873326701527100
            yt_1 = 1122971360415723681
            yt_serdar = 1122971360415723682
            yt_elite = 1122971360415723683
            yt_legend = 1122971360415723684
            booster = 675282018954641409

            has_special_role_id_1 = any(
                role.id == special_role_id_1 for role in message.author.roles
            )
            yt_1 = any(role.id == special_role_id_1 for role in message.author.roles)
            yt_serdar = any(
                role.id == special_role_id_1 for role in message.author.roles
            )
            yt_elite = any(
                role.id == special_role_id_1 for role in message.author.roles
            )
            yt_legend = any(
                role.id == special_role_id_1 for role in message.author.roles
            )
            booster = any(role.id == special_role_id_1 for role in message.author.roles)

            if user_balance is not None:
                reward = 50
                balance = user_balance + reward

                if has_special_role_id_1:
                    balance += int(reward * 0.5)
                elif yt_1:
                    balance += int(reward * 1)
                elif yt_serdar:
                    balance += int(reward * 1.5)
                elif yt_elite and booster:
                    balance += int(reward * 2)
                elif yt_legend:
                    balance += int(reward * 3.5)

                await self.update_user_balance(user_id, balance)

    @commands.command()
    async def balance(self, ctx: commands.Context):
        user_id = ctx.author.id
        user_balance = await self.get_user_balance(user_id)
        if user_balance is not None:
            balance_display = f"{self.currency_icon} {user_balance}"
            await ctx.send(f"Your balance is: {balance_display}")
        else:
            await ctx.send(
                "You don't have an account. Use the `register` command to create one."
            )

    @commands.command()
    async def register(self, ctx: commands.Context):
        user_id = ctx.author.id
        try:
            query = "INSERT INTO economy (user_id, balance) VALUES (%s, 0)"
            values = (user_id,)
            cursor = self.bot.db.cursor()
            cursor.execute(query, values)
            self.bot.db.commit()
            cursor.close()
            await ctx.send("Account registered successfully!")
        except ProgrammingError:
            await ctx.send("Account already registered!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_money(self, ctx: commands.Context, user: discord.Member, amount: int):
        user_balance = await self.get_user_balance(user.id)

        if user_balance is not None:
            new_balance = user_balance + amount
            await self.update_user_balance(user.id, new_balance)
            await ctx.send(
                f"{amount} {self.currency_icon} added to {user.display_name}'s balance. New balance: {new_balance}"
            )
        else:
            await ctx.send(
                f"{user.display_name} doesn't have an account. They can use the `register` command to create one."
            )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset_balance(self, ctx: commands.Context, user: discord.Member):
        user_balance = await self.get_user_balance(user.id)

        if user_balance is not None:
            new_balance = (user_balance * 0) + 50
            await self.update_user_balance(user.id, new_balance)
            await ctx.send(
                f"> The balance has been reset. New Balance {self.currency_icon} {new_balance}"
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
