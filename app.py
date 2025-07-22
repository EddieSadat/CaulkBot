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

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

openai.api_key = os.getenv("OPENAI_KEY")

headers = {'content-type': 'application/json',
           'authorization': f'Bearer {os.getenv("COC_KEY")}'}

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents = intents)


def normalWar():
    response = requests.get(
        "https://api.clashofclans.com/v1/clans/%232LV8CPL89/currentwar",
        headers = headers)
    data = response.json()

    # ==== Normal War in progress ====
    if data['state'] == 'inWar':
        # ==== Clan details ====
        total_stars = data['teamSize'] * 3
        
        clan_name = data['clan']['name']
        clan_level = data['clan']['clanLevel']
        clan_stars = data['clan']['stars']
        clan_destruction = data['clan']['destructionPercentage']

        opp_name = data['opponent']['name']
        opp_level = data['opponent']['clanLevel']
        opp_stars = data['opponent']['stars']
        opp_destruction = data['opponent']['destructionPercentage']

        # ==== Win/Loss status
        status = None
        if clan_stars > opp_stars: # Stars winning
            status = ':smile:'
        elif clan_stars < opp_stars: # Stars losing
            status = ':cry:'
        elif clan_stars == opp_stars and clan_stars > opp_stars: # Stars tied but percent winning
            status = ':smile:'
        elif clan_stars == opp_stars and clan_stars < opp_stars: # Stars tied but percent losing
            status = ':cry:'
        elif clan_stars == opp_stars and clan_stars == opp_stars: # Stars and percent tied
            status = ':exploding_head:'

        # ==== Time remaining ====
        timestamp = data['endTime']

        time_end = datetime.strptime(timestamp, '%Y%m%dT%H%M%S.%fZ')
        time_now = datetime.now(timezone.utc) 

        time_remain = (time_end - time_now).total_seconds()
        time_remain_hours, time_remain = divmod(time_remain, 60*60)
        time_remain_min, time_remain_sec = divmod(time_remain, 60)

        # ==== Attack details ====
        clan_members = data['clan']['members']
        clanDf = pd.json_normalize(clan_members)
        clanDf = clanDf.sort_values(by='mapPosition', axis=0).reset_index(drop=True)
        clanDf['attacks'] = clanDf['attacks'].fillna('')

        clanDf['numAttacks'] = clanDf['attacks'].str.len()
        clanDf

        attack1 = []
        attack2 = []
        players = []
        players_missing_attacks = []

        for ind in clanDf.index:
            players.append(clanDf['name'][ind])

            if  clanDf['numAttacks'][ind] == 0:
                attack1.append('✖️✖️✖️')
                attack2.append('✖️✖️✖️')
                players_missing_attacks.append(clanDf['name'][ind])

            elif clanDf['numAttacks'][ind] == 1:
                if clanDf['attacks'][ind][0]['stars'] == 0:
                    attack1.append('➖➖➖')
                elif clanDf['attacks'][ind][0]['stars'] == 1:
                    attack1.append('⭐➖➖')
                elif clanDf['attacks'][ind][0]['stars'] == 2:
                    attack1.append('⭐⭐➖')
                elif clanDf['attacks'][ind][0]['stars'] == 3:
                    attack1.append('⭐⭐⭐')

                attack2.append('✖️✖️✖️')
                players_missing_attacks.append(clanDf['name'][ind])

            elif clanDf['numAttacks'][ind] == 2:
                for attack in range(len(clanDf['attacks'][ind])):
                    if attack == 0:
                        if clanDf['attacks'][ind][attack]['stars'] == 0:
                            attack1.append('➖➖➖')
                        elif clanDf['attacks'][ind][attack]['stars'] == 1:
                            attack1.append('⭐➖➖')
                        elif clanDf['attacks'][ind][attack]['stars'] == 2:
                            attack1.append('⭐⭐➖')
                        elif clanDf['attacks'][ind][attack]['stars'] == 3:
                            attack1.append('⭐⭐⭐')

                    elif attack == 1:
                        if clanDf['attacks'][ind][attack]['stars'] == 0:
                            attack2.append('➖➖➖')
                        elif clanDf['attacks'][ind][attack]['stars'] == 1:
                            attack2.append('⭐➖➖')
                        elif clanDf['attacks'][ind][attack]['stars'] == 2:
                            attack2.append('⭐⭐➖')
                        elif clanDf['attacks'][ind][attack]['stars'] == 3:
                            attack2.append('⭐⭐⭐')


        clanDf['attack1'] = attack1
        clanDf['attack2'] = attack2

        attack1 = "\n".join(attack1)
        attack2 = "\n".join(attack2)
        players = "\n".join(players)

    # ==== Normal War preperation ====
    elif data['state'] == 'preparation':
        # ==== Clan details ====
        total_stars = data['teamSize'] * 3
        
        clan_name = data['clan']['name']
        clan_level = data['clan']['clanLevel']

        opp_name = data['opponent']['name']
        opp_level = data['opponent']['clanLevel']

        # ==== Time remaining ====
        timestamp = data['startTime']

        time_start = datetime.strptime(timestamp, '%Y%m%dT%H%M%S.%fZ')
        time_now = datetime.now(timezone.utc) 

        time_remain = (time_start - time_now).total_seconds()
        time_remain_hours, time_remain = divmod(time_remain, 60*60)
        time_remain_min, time_remain_sec = divmod(time_remain, 60)




    # else:
    #     response = requests.get(
    #         "https://api.clashofclans.com/v1/clans/%232LV8CPL89/currentwar",
    #         headers = headers)
    #     data = response.json()
        






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