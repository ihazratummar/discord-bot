import discord
from discord.ext import commands
from discord import app_commands
from asyncpg import Record
from config import Bot
from typing import Dict
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
from pilmoji import Pilmoji
import asyncio


class Economy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.currency_icon = "💰"
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

    async def create_balance_banner(self, member: discord.Member, balance: int):
        # Load the user's avatar
        avatar_url = member.avatar.url
        avatar_response = requests.get(avatar_url)
        avatar_data = BytesIO(avatar_response.content)
        avatar_image = Image.open(avatar_data).convert("RGBA")

        # Resize the avatar
        avatar_image = avatar_image.resize((100, 100), Image.ANTIALIAS)

        # Create a circular mask for the avatar
        mask = Image.new("L", (100, 100), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 100, 100), fill=255)
        avatar_image.putalpha(mask)

        # Create a blank image for the banner
        banner_width = 400
        banner_height = 128
        banner = Image.new("RGB", (banner_width, banner_height), (0, 0, 0))

        draw = ImageDraw.Draw(banner)

        gradient_start = (0, 146, 69)  # Dark green
        gradient_end = (252, 238, 33)  # Yellow
        for y in range(banner_height):
            r = int(
                gradient_start[0]
                + (gradient_end[0] - gradient_start[0]) * y / banner_height
            )
            g = int(
                gradient_start[1]
                + (gradient_end[1] - gradient_start[1]) * y / banner_height
            )
            b = int(
                gradient_start[2]
                + (gradient_end[2] - gradient_start[2]) * y / banner_height
            )
            draw.line([(0, y), (banner_width, y)], fill=(r, g, b))

        # Load a font (adjust the path to your font file)
        font = ImageFont.truetype("Lato-Bold.ttf", 24)

        # Paste the user's avatar on the right side
        avatar_x = banner_width - 128
        avatar_y = (banner_height - avatar_image.height) // 2
        banner.paste(avatar_image, (avatar_x, avatar_y), avatar_image)

        # Add text for the balance
        balance_text = f"Balance: {self.currency_icon} {balance}"
        text_width, text_height = draw.textsize(balance_text, font, font)
        text_x = (banner_width - text_width - 150) // 2  # Adjust the position as needed
        text_y = (banner_height - text_height) // 2  # Center vertically
        with Pilmoji(banner) as pilmoji:
            pilmoji.text((text_x, text_y), balance_text, fill=(0, 0, 0), font=font)

        return banner

    @app_commands.command(name="balance", description="Check balance")
    async def balance(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        user_balance = await self.load_user_balances()

        if user_id in user_balance:
            user_balance = user_balance[user_id]

            # Assuming you have a function create_balance_banner that creates the banner
            banner = await self.create_balance_banner(interaction.user, user_balance)

            # Save the banner image to a file
            banner_path = "balance_banner.png"
            banner.save(banner_path)

            # Send the banner as a file and then remove it after a small delay
            with open(banner_path, "rb") as f:
                await interaction.response.send_message(
                    file=discord.File(f, "balance_banner.png")
                )

            f.close()

            # Introduce a delay before removing the temporary file
            await asyncio.sleep(1)
            os.remove(banner_path)  # Remove the temporary file
        else:
            await interaction.response.send_message(
                "You don't have an account. Use the `.register` command to create one."
            )

    @app_commands.command()
    async def register(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        user_balances = await self.load_user_balances()

        if user_id not in user_balances:
            user_balances[user_id] = 0
            await self.save_user_balances(user_balances)
            await interaction.response.send_message("Account has been registered")
        else:
            await interaction.response.send_message("Account already registered!")

    @app_commands.command()
    async def remove_account(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        user_balances = await self.load_user_balances()

        if user_id in user_balances:
            del user_balances[user_id]
            await self.save_user_balances(user_balances)
            await interaction.response.send_message("Account removed")
        else:
            await interaction.response.send_message(
                "You don't have an account to remove."
            )

    @app_commands.command(
        name="add_money", description="Adds money to a user's balance"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def add_money(
        self, interaction: discord.Interaction, user: discord.User, balance: int
    ):
        user_id = str(user.id)
        user_balances = await self.load_user_balances()

        if user_id in user_balances:
            user_balances[user_id] += balance
            await self.save_user_balances(user_balances)
            new_balance = user_balances[user_id]
            await interaction.response.send_message(
                f"{self.currency_icon} {balance} added to {user.display_name}'s balance. New balance: {new_balance}"
            )
        else:
            await interaction.response.send_message(
                f"{user.display_name} does not exist"
            )

    @add_money.error
    async def add_money_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "> Give the required information | Ex - `.add_money @username 200` "
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
