import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from config import Bot
from datetime import datetime, timedelta
from discord.app_commands import Choice


class General(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @app_commands.command()
    # #@app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    # async def hi(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(f"Hi how are you")

    @app_commands.command(name="ping", description="server ping")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Ping {round(bot.latency * 1000)} ms")

    @app_commands.command(name="quota", description="Display quota")
    async def quota(self, interaction: discord.Interaction):
        responses = requests.get("https://api.quotable.io/random")
        data = responses.json()
        quota = data["content"]
        author = data["author"]
        await interaction.response.send_message(f"{author}:\n\n━━━━{quota}")

    @app_commands.command(name="wiki", description="Search wikipedia")
    async def wiki(self, interaction: discord.Interaction, query: str):
        import wikipedia

        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=2)
        await interaction.response.send_message(result)

    @app_commands.command(
        name="pc", description="Check my Gaming and Streaming pc Config"
    )
    async def pc(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Gaming PC\n\nCPU:- Ryzen 7 3700x.\nGraphics Card:- 2060 super 8gb.\nMemory - XPG 16GB 3600MHz\nStorage - 1 TB SSD /1TB HDD\n\nStreaming PC\n\nCPU: Intel i3 7th gen\nGPU: 1050Ti 4GB OC\nRAM: 8 GB 2400 MHz\nStorage: 250 GB SSD\nElgato HD60s 14000\nTotal Price:-124500"
        )

    @app_commands.command(
        name="whatsapp", description="whatsapp  group daily stream notification"
    )
    async def whatsapp(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Join Whatsapp Group for stream notification : https://bit.ly/3zBxoCf"
        )

    @app_commands.command(name="support")
    async def support(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"You can support us by becoming a facebook page member.\nBecome a supporter:-  https://bit.ly/3xJdNzZ"
        )

    @app_commands.command(name="social")
    async def social(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"You can check all my social profile here :\nhttps://wlo.link/@crazyforsurprise"
        )

        # Send the meme to the Discord channel
        await interaction.response.send_message(file=file)

    @app_commands.command(name="youtube", description="search video")
    async def youtube(self, interaction: discord.Interaction, search: str):
        response = requests.get(f"https://youtube.com/results?search_query={search}")
        html = response.text
        index = html.find("/watch?v=")
        url = "https://www.youtube.com" + html[index : index + 20]
        await interaction.response.send_message(url)

    @app_commands.command(name="imgur", description="search for images")
    async def imgur(self, interaction: discord.Interaction, *, query: str):
        headers = {"Authorization": "Client-ID 20c2904655c6a1f"}
        params = {"q": query}
        response = requests.get(
            "https://api.imgur.com/3/gallery/search/", headers=headers, params=params
        )

        if response.status_code == 200:
            data = json.loads(response.content.decode("utf-8"))
            images = [
                item for item in data["data"] if "images" in item and item["images"]
            ]

            if images:
                random_image = random.choice(images)
                image_url = random.choice(random_image["images"])["link"]

                embed = discord.Embed(
                    title=f'Results for "{query}"', color=discord.Color.blue()
                )
                embed.set_image(url=image_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    f'Sorry, no images found for "{query}"'
                )
        else:
            await interaction.response.send_message(
                "Sorry, there was an error processing your request. Please try again later."
            )

    @app_commands.command(name="invite", description="Invite Link")
    async def invite(self, interaction: discord.Interaction):
        link = await interaction.channel.create_invite(max_age=0)
        await interaction.response.send_message(link)

    @app_commands.command(name="pick", description="Choose between multiple options")
    async def pick(self, interaction: discord.Interaction, options: str):
        option_list = options.split()
        if len(option_list) < 2:
            await interaction.response.send_message("please provide at least 2 options")
            return

        chosen_option = random.choice(option_list)
        embed = discord.Embed(
            title="Choice",
            description=f"Chosen option: {chosen_option}",
            color=discord.Color.random(),
        )
        embed.add_field(name="Options", value="\n".join(option_list), inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="flip", description="flip a coin")
    async def flip(self, interaction: discord.Interaction):
        random_side = random.randint(0, 1)
        if random_side == 1:
            await interaction.response.send_message("Head")
        else:
            await interaction.response.send_message("Tail")


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
