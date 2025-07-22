import discord
from discord.ext import commands, tasks
# import nest_asyncio
import requests
from datetime import datetime, timezone
import pandas as pd
import openai
# import json
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()


openai.api_key = os.getenv("OPENAI_KEY")

headers = {'content-type': 'application/json',
           'authorization': f'Bearer {os.getenv("COC_KEY")}'}

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents = intents)



response = requests.get(
    "https://api.clashofclans.com/v1/clans/%232LV8CPL89/currentwar",
    headers = headers)
data = response.json()
    

@bot.event
async def on_ready():
    print("online")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await message.channel.send('Oi oi oi')



bot.run(os.getenv("DISCORD_KEY"))