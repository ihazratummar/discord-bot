from ummaroyin import *
from http.client import *
from urllib import *
import requests
import random
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands
from client import *


@client.event
async def on_ready():
    print('Bot is ready.')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)   
        
@client.tree.command(name="ping", description = "Check your ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(client.latency * 1000)}ms')   

@client.tree.command(name="quota", description = "Display quota")
async def quota(interaction: discord.Interaction):
    responses = requests.get("https://api.quotable.io/random")
    data = responses.json()
    quota = data["content"]
    author = data["author"]
    await interaction.response.send_message(f"{author}:\n\n━━━━{quota}")    
    
@client.tree.command(name="wiki", description = "Search wikipedia")
async def wiki(interaction: discord.Interaction, query: str):
    import wikipedia
    wikipedia.set_lang("en")
    result = wikipedia.summary(query, sentences=2)
    await interaction.response.send_message(result)           

@client.tree.command(name="pc", description="Check my Gaming and Streaming pc Config")
async def pc(interaction: discord.Interaction):
    await interaction.response.send_message(f"Gaming PC\n\nCPU:- Ryzen 7 3700x.\nGraphics Card:- 2060 super 8gb.\nMemory - XPG 16GB 3600MHz\nStorage - 1 TB SSD /1TB HDD\n\nStreaming PC\n\nCPU: Intel i3 7th gen\nGPU: 1050Ti 4GB OC\nRAM: 8 GB 2400 MHz\nStorage: 250 GB SSD\nElgato HD60s 14000\nTotal Price:-124500") 

@client.tree.command(name="whatsapp", description="whatsapp  group daily stream notification")
async def whatsapp(interaction: discord.Interaction):
    await interaction.response.send_message(f'Join Whatsapp Group for stream notification : https://bit.ly/3zBxoCf')

@client.tree.command(name="support")
async def support(interaction: discord.Interaction):
    await interaction.response.send_message(f'You can support us by becoming a facebook page member.\nBecome a supporter:-  https://bit.ly/3xJdNzZ') 

@client.tree.command(name="social")
async def social(interaction: discord.Interaction):
    await interaction.response.send_message(f'You can check all my social profile here :\nhttps://wlo.link/@crazyforsurprise') 
