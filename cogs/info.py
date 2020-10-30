import discord
import json
import asyncio
import requests
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from pathlib import Path

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def status(self ,ctx):

        await ctx.trigger_typing()
        URL = "http://serverstatus.albiononline.com/"
        a = requests.get(url = URL, timeout=30)
        a.encoding = "utf-8"
        a = a.text
        a = a.replace('\n', ' ').replace("\r", '').replace('\ufeff', '')
        data = json.loads(a) #{ "status": "online", "message": "All good." }
        #try:
        #except:
            #await ctx.send("Server connection timeout, there's propably a maintenance.")
        if data['status'] == 'offline':
            embed = discord.Embed(
            colour = discord.Colour.red(),
            )
        else:
            embed = discord.Embed(
            colour = discord.Colour.green(),
            )

        embed.add_field(name='Status: {}'.format(data['status']), value=data['message'], inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(info(client))