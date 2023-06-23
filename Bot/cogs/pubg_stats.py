import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from config import Bot
import json
import os
import requests


load_dotenv()
pubg_api_key = os.getenv("PUBG_API_KEY")


class PubgStats(commands.Cog):
    def __init__(self, bot: Bot, player_name):
        self.bot = bot
        self.player_name = player_name

    @tasks.loop(seconds=60)  # Adjust the interval as needed
    async def fetch_and_post_pubg_stats(self):
        # Fetch PUBG stats using the API and post them to Discord
        headers = {"Authorization": pubg_api_key}  # Replace with your PUBG API key
        response = requests.get(
            f"https://api.example.com/pubg/players/{self.player_name}/matches",
            headers=headers,
        )
        if response.status_code == 200:
            matches = json.loads(response.text)
            # Process the matches and find the latest match of the player
            latest_match = self.find_latest_match(matches, self.player_name)
            if latest_match is not None:
                match_stats = self.get_match_stats(latest_match)
                if match_stats is not None:
                    formatted_stats = self.format_stats(match_stats)
                    channel = self.bot.get_channel(
                        874162166343815229
                    )  # Replace CHANNEL_ID with the actual channel ID where you want to post the stats
                    await channel.send(formatted_stats)

    @staticmethod
    def find_latest_match(matches, player_name):
        # Filter matches for the specified player
        player_matches = [
            match for match in matches if match["player_name"] == player_name
        ]

        # Sort the matches by date in descending order
        sorted_matches = sorted(player_matches, key=lambda x: x["date"], reverse=True)

        # Return the latest match if available
        if sorted_matches:
            return sorted_matches[0]

        return None

    @staticmethod
    def get_match_stats(match):
        # Extract the desired match stats
        if "kills" in match:
            total_kills = match["kills"]
        else:
            total_kills = 0

        if "deaths" in match:
            total_deaths = match["deaths"]
        else:
            total_deaths = 0

        if "map" in match:
            map_name = match["map"]
        else:
            map_name = "Unknown"

        # Calculate the kill-death ratio (KD)
        if total_deaths > 0:
            kd_ratio = total_kills / total_deaths
        else:
            kd_ratio = 0.0

        # Return the match stats
        return {
            "player_name": match["player_name"],
            "total_kills": total_kills,
            "kd_ratio": kd_ratio,
            "map_name": map_name,
        }

    @staticmethod
    def format_stats(stats):
        formatted_stats = f"Player: {stats['player_name']}\n"
        formatted_stats += f"Total Kills: {stats['total_kills']}\n"
        formatted_stats += f"KD Ratio: {stats['kd_ratio']:.2f}\n"
        formatted_stats += f"Map: {stats['map_name']}\n"
        return formatted_stats


player_name = "crazyforsurprise"


async def setup(bot: commands.Bot):
    await bot.add_cog(PubgStats(bot, player_name))
