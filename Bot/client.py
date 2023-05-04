from http import client
from http.client import *
import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()

client = commands.Bot(command_prefix='!', intents=intents)