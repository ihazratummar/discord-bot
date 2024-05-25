import discord
from discord.ext import commands
import requests
from config import Bot


class Crypto(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="crypto")
    async def crypto_command(self, ctx, symbol: str):
        """Fetch cryptocurrency details."""
        try:
            # You can replace this API with the one you prefer.
            api_url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}"
            response = requests.get(api_url)
            data = response.json()

            if "error" in data:
                await ctx.send(f"Error: {data['error']}")
            else:
                name = data.get("name", "N/A")
                symbol = data.get("symbol", "N/A")
                current_price = (
                    data.get("market_data", {})
                    .get("current_price", {})
                    .get("usd", "N/A")
                )

                await ctx.send(f"{name} ({symbol}) - Current Price: ${current_price}")
        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred: {str(e)}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {str(e)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Crypto(bot))
