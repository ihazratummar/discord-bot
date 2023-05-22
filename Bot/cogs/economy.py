import discord
from discord.ext import commands
from asyncpg import Record
from config import Bot
from discord import app_commands
from typing import Dict
import mysql.connector
from mysql.connector.errors import ProgrammingError


class Economy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.currency_icon = "💵"

    async def get_user_balance(self, user_id: str):
        query = "SELECT balance FROM economy WHERE user_id = %(user_id)s"
        values = {"user_id": user_id}
        results = await self.execute_query(query, values)
        return results[0] if results else None

    async def update_user_balance(self, user_id: str, balance: int):
        query = "UPDATE economy SET balance = %(balance)s WHERE user_id = %(user_id)s"
        values = {"user_id": user_id, "balance": balance}
        await self.execute_query(query, values)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.content.startswith(
            self.bot.command_prefix
        ):  # Ignore messages from bots
            user_id = str(message.author.id)
            user_data = await self.get_user_balance(user_id)
            if user_data:
                balance = user_data["balance"]
                balance += 10
                await self.update_user_balance(user_id, balance)

    @app_commands.command()
    async def balance(self, interaction: discord.Interaction):
        """Check the user's balance"""
        user_id = str(ctx.author.id)
        user_data = await self.get_user_balance(user_id)
        if user_data:
            balance = user_data["balance"]
            balance_display = f"{self.currency_icon} {balance}"
            await ctx.send(f"Your balance is: {balance_display}")
        else:
            await ctx.send("You don't have an account. Use `!register` to create one.")

    @commands.command()
    async def register(self, ctx):
        """Register an account"""
        user_id = str(ctx.author.id)
        query = "INSERT INTO economy (user_id, balance) VALUES (%(user_id)s, 0) ON DUPLICATE KEY UPDATE balance = balance"
        values = {"user_id": user_id}
        await self.execute_query(query, values)
        await ctx.send("Account registered successfully!")

    @commands.command()
    async def deposit(self, ctx, amount: int):
        """Deposit coins into your account"""
        if amount <= 0:
            await ctx.send("Please enter a valid amount to deposit.")
            return

        user_id = str(ctx.author.id)
        query = "UPDATE economy SET balance = balance + %(amount)s WHERE user_id = %(user_id)s"
        values = {"amount": amount, "user_id": user_id}
        await self.execute_query(query, values)
        await ctx.send(f"You have deposited {amount} coins.")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        """Withdraw coins from your account"""
        if amount <= 0:
            await ctx.send("Please enter a valid amount to withdraw.")
            return

        user_id = str(ctx.author.id)
        user_data = await self.get_user_balance(user_id)
        if not user_data:
            await ctx.send("You don't have an account. Use `!register` to create one.")
            return

        balance = user_data["balance"]
        if amount > balance:
            await ctx.send("Insufficient funds.")
            return

        balance -= amount
        await self.update_user_balance(user_id, balance)
        await ctx.send(f"You have withdrawn {amount} coins.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
