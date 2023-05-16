import discord
from discord.ext import commands
from client import bot
import os
import random


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    await channel.send(f"Welcome to the server, {member.mention}!")
