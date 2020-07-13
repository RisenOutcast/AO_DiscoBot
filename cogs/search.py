import discord
import json
import asyncio
import requests
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from pathlib import Path

class search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True,aliases=['Player'])
    async def player(self ,ctx, *, player : str = None):

        print('Searching for player ' + str(player))
        await ctx.trigger_typing()

        URL = 'https://gameinfo.albiononline.com/api/gameinfo/search?q={}'.format(player)
        a = requests.get(url = URL)
        data = a.json()

        #Create a embed
        embed = discord.Embed(
        colour = discord.Colour.blue(),
        )

        print('--------------------------------------')
        print(data['players'][0]['Name'])
        embed.set_author(name=data['players'][0]['Name'])

        try:
            if str(data['players'][0]['GuildName']) is None:
                    print('No Guild')
                    embed.add_field(name='Guild', value='Not in a guild', inline=True)
            else:
                if str(data['players'][0]['GuildName']) is '':
                    print('No Guild')
                    embed.add_field(name='Guild', value='Not in a guild', inline=True)
                else:
                    print(data['players'][0]['GuildName'])
                    embed.add_field(name='Guild', value=data['players'][0]['GuildName'], inline=True)
        except:
            print('No Guild')
            embed.add_field(name='Guild', value='Not in a guild', inline=True)

        try:
            if str(data['players'][0]['AllianceName']) is None:
                print('No Alliance')
                embed.add_field(name='Alliance', value='Not in a alliance', inline=True)
            else:
                if str(data['players'][0]['AllianceName']) is '':
                    print('No Alliance')
                    embed.add_field(name='Alliance', value='Not in a alliance', inline=True)
                else:
                    URL3= 'https://gameinfo.albiononline.com/api/gameinfo/alliances/{}'.format(data['players'][0]['AllianceId']) #Alliance info
                    c = requests.get(url = URL3)
                    data3 = c.json()

                    print(data3['AllianceName'])
                    print(data['players'][0]['AllianceName'])
                    embed.add_field(name='Alliance', value=('[' + str(data['players'][0]['AllianceName']) + '] ' + str(data3['AllianceName'])), inline=True)
        except:
            print('No Alliance')
            embed.add_field(name='Alliance', value='Not in a alliance', inline=True)


        #embed.add_field(name='Kill Fame', value=data['players'][0]['KillFame'], inline=False)
        #embed.add_field(name='Death Fame', value=data['players'][0]['DeathFame'], inline=False)
        #embed.add_field(name='Fame Ratio', value=data['players'][0]['FameRatio'], inline=False)
        #embed.add_field(name='Total Kills', value=data['players'][0]['totalKills'], inline=False)
        #embed.add_field(name='GvG Kills', value=data['players'][0]['gvgKills'], inline=False)
        #embed.add_field(name='GvG Wins', value=data['players'][0]['gvgWon'], inline=False)
        embed.add_field(name='Stats',value='**Kill Fame**: ' + str(self.comma_me(data['players'][0]['KillFame'])) + '\n' + '**Death Fame**: ' + str(self.comma_me(data['players'][0]['DeathFame'])) + '\n' + '**Fame Ratio**: ' + str(data['players'][0]['FameRatio']) + '\n ' + '**Total Kills**: ' + str(self.comma_me(data['players'][0]['totalKills'])) + '\n ' + '**GvG Kills**: ' + str(self.comma_me(data['players'][0]['gvgKills'])) + '\n ' + '**GvG Wins**: ' + str(self.comma_me(data['players'][0]['gvgWon'])), inline=False)
        #embed.add_field(name='Value',value=str(data['players'][0]['KillFame']) + '\n' + str(data['players'][0]['DeathFame']) + '\n' + str(data['players'][0]['FameRatio']) + '\n' + str(data['players'][0]['totalKills']) + '\n' + str(data['players'][0]['gvgKills']) + '\n' + str(data['players'][0]['gvgWon']), inline=True)
        print(data['players'][0]['KillFame'])
        print(data['players'][0]['DeathFame'])
        print(data['players'][0]['FameRatio'])
        print(data['players'][0]['totalKills'])
        print(data['players'][0]['gvgKills'])
        print(data['players'][0]['gvgWon'])

        URL2 = 'https://gameinfo.albiononline.com/api/gameinfo/players/{}'.format(data['players'][0]['Id']) #Complete player info
        b = requests.get(url = URL2)
        data2 = b.json()

        embed.add_field(name='PvE Fame', value=self.comma_me(data2['LifetimeStatistics']['PvE']['Total']), inline=False)
        embed.add_field(name='Gathering Fame', value=self.comma_me(data2['LifetimeStatistics']['Gathering']['All']['Total']), inline=False)
        embed.add_field(name='Crafting Fame', value=self.comma_me(data2['LifetimeStatistics']['Crafting']['Total']), inline=False)
        print(self.comma_me(data2['LifetimeStatistics']['PvE']['Total']))
        print(self.comma_me(data2['LifetimeStatistics']['Gathering']['All']['Total']))
        print(self.comma_me(data2['LifetimeStatistics']['Crafting']['Total']))
        print(self.comma_me(data2['LifetimeStatistics']['CrystalLeague']))

        await ctx.send(embed=embed)

    #Make numbers more human-friendly
    def comma_me(self, number): 
        if number is None:
            return
        else:
            if number is '':
                return
            else:
                return ("{:,}".format(number)) 
  
    

def setup(client):
    client.add_cog(search(client))