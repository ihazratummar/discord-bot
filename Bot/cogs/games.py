import random
import discord
import config
from discord import app_commands
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, bot: config.Bot):
        self.bot = bot

    @commands.command(name="guess_number", description="Guess the number")
    async def guess_number(self, ctx: commands.Context):
        number = random.randint(1, 20)
        await ctx.send("Welcome to the number guessing game! Guess a number between 0 and 20.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        tries = 0
        while True:
            try:
                guess = await self.bot.wait_for('message', check=check, timeout=30)
                guess_number = int(guess.content)
                tries += 1

                if guess_number == number:
                    await ctx.send(f"Congratulations! You guessed the number in {tries} tries.")
                    break
                elif guess_number < number:
                    await ctx.send("Too low! Try again.")
                else:
                    await ctx.send("Too high! Try again.")
            except ValueError:
                await ctx.send("Invalid input. Please enter a valid number.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
