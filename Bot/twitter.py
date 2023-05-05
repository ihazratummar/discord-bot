import os
import tweepy
import discord
from dotenv import load_dotenv
from client import *

load_dotenv()

# Set up Twitter API credentials
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

# Set up Twitter API authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up Twitter API client
api = tweepy.API(auth)

# Define the Twitter user(s) to track
twitter_usernames = ["ummaroyin"]

# Define the Discord channel to send notifications to
discord_channel_id = 874162166343815229

# Set up Discord client
# client = discord.Client()

# Send notifications for new tweets
@client.event
async def on_ready():
    print("Bot is ready.")
    channel = client.get_channel(discord_channel_id)
    for username in twitter_usernames:
        user = api.get_user(screen_name=username)
        tweets = api.user_timeline(screen_name=username, count=1)
        for tweet in tweets:
            tweet_id = tweet.id
            tweet_text = tweet.text
            tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
            await channel.send(f"@everyone {username} {tweet_text}\n{tweet_url}")
            
on_ready()            
