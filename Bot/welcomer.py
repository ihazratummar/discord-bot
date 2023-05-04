import discord
from discord.ext import commands
from io import BytesIO
from config import *
import json
import easy_pil
from easy_pil import Editor, load_async, Font

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Bot Is Online")
    
@client.event
async def on_member_join(member):
    
    channel = client.get_channel(540205113575473164)
    
    background = Editor("background.jpg")
    profile_image = await load_async(str(member.avatar_url))

    profile = Editor(profile_image).resize((150,150)).circle_image()
    poppins = Font.poppins(size=50, variant="bold")
    
    poppins_small = Font.poppins(size=20, variant="light")
    
    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)
    
    background.text((400,160), f"Welcome To {member.guild.name}", color= "white", font = poppins, align = "center")
    background.text((400,265), f"{member.name}#{member.discriminator}", color= "white", font = poppins_small, align = "center")
    
    file = discord.File(fp=BytesIO(background.image_bytes()), filename="background.jpg")
    await channel.send(f"Hello {member.mention}! Welcome to **{member.guild.name} for more information go to #rules**")
    await channel.send(file=file)