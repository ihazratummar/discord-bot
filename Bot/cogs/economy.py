import discord
from discord.ext import commands
from asyncpg import Record
from config import Bot
from discord import app_commands


class Economy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.currency_icon = "💵"

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.content.startswith(
            self.bot.command_prefix
        ):  # Ignore messages from bots
            user_id = str(message.author.id)
            query = "UPDATE economy SET balance = balance + $1 WHERE user_id = $2"
            await self.bot.db.execute(
                query,
                10,
                user_id,
            )

    @app_commands.command()
    async def balance(self, interaction: discord.Interaction):
        """Check the user's balance"""
        user_id = str(interaction.user.id)
        query = "SELECT balance FROM economy WHERE user_id = $1"
        record: Record = await self.bot.db.fetchrow(query, user_id)
        if record:
            balance = record["balance"]
            balance_display = f"{self.currency_icon} {balance}"
            await interaction.response.send_message(
                f"Your balance is: {balance_display}"
            )
        else:
            await interaction.response.send_message(
                "You don't have an account. Use `!register` to create one."
            )

    @commands.command()
    async def register(self, ctx):
        """Register an account"""
        user_id = str(ctx.author.id)
        query = "INSERT INTO economy (user_id, balance) VALUES ($1, 0) ON CONFLICT DO NOTHING"
        await self.bot.db.execute(query, user_id)
        await ctx.send("Account registered successfully!")

    @commands.command()
    async def deposit(self, ctx, amount: int):
        """Deposit coins into your account"""
        if amount <= 0:
            await ctx.send("Please enter a valid amount to deposit.")
            return

        user_id = str(ctx.author.id)
        query = "UPDATE economy SET balance = balance + $1 WHERE user_id = $2"
        await self.bot.db.execute(query, amount, user_id)
        await ctx.send(f"You have deposited {amount} coins.")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        """Withdraw coins from your account"""
        if amount <= 0:
            await ctx.send("Please enter a valid amount to withdraw.")
            return

        user_id = str(ctx.author.id)
        query = "SELECT balance FROM economy WHERE user_id = $1"
        record: Record = await self.bot.db.fetchrow(query, user_id)
        if not record:
            await ctx.send("You don't have an account. Use `!register` to create one.")
            return

        balance = record["balance"]
        if amount > balance:
            await ctx.send("Insufficient funds.")
            return

        query = "UPDATE economy SET balance = balance - $1 WHERE user_id = $2"
        await self.bot.db.execute(query, amount, user_id)
        await ctx.send(f"You have withdrawn {amount} coins.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
