import discord
from discord.ext import commands
from asyncpg import Record
from config import Bot
from discord import app_commands
from typing import Dict
import json
import os


class Economy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.currency_icon = "💵"
        self.user_balances_file = "Bot/cogs/Rewards/user_balances.json"

    async def load_user_balances(self):
        if os.path.exists(self.user_balances_file):
            with open(self.user_balances_file, "r") as f:
                return json.load(f)
        else:
            return {}

    async def save_user_balances(self, balances):
        with open(self.user_balances_file, "w") as f:
            json.dump(balances, f, indent=4)

    async def get_user_balance(self, user_id: int):
        user_balances = await self.load_user_balances()
        return user_balances.get(str(user_id))

    async def update_user_balance(self, user_id: int, balance: int):
        user_balances = await self.load_user_balances()
        user_balances[str(user_id)] = balance
        await self.save_user_balances(user_balances)

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
        user_id = str(ctx.author.id)
        user_balances = await self.load_user_balances()

        if user_id in user_balances:
            user_balance = user_balances[user_id]
            balance_display = f"{self.currency_icon} {user_balance}"
            await ctx.send(f"Your balance is: {balance_display}")
        else:
            await ctx.send(
                "You don't have an account. Use the `register` command to create one."
            )

    @commands.command()
    async def register(self, ctx: commands.Context):
        user_id = ctx.author.id
        user_balances = await self.load_user_balances()

        if user_id not in user_balances:
            user_balances[user_id] = 0
            await self.save_user_balances(user_balances)
            await ctx.send("Account registered successfully")
        else:
            await ctx.send("Account already registered!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_money(self, ctx: commands.Context, user: discord.Member, amount: int):
        user_id = str(user.id)
        user_balances = await self.load_user_balances()

        if user_id in user_balances:
            user_balances[user_id] += amount
            await self.save_user_balances(user_balances)
            new_balance = user_balances[user_id]
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
        user_id = str(user.id)
        user_balances = await self.load_user_balances()

        if user_id in user_balances:
            user_balances[user_id] = 50  # Reset to 50
            await self.save_user_balances(user_balances)
            new_balance = user_balances[user_id]
            await ctx.send(
                f"> The balance has been reset. New Balance {self.currency_icon} {new_balance}"
            )
        else:
            await ctx.send(
                f"{user.display_name} doesn't have an account. They can use the `register` command to create one."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
