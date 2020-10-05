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

    @commands.command(pass_context=True,aliases=['Player'])
    async def status(self ,ctx, *, player : str = None):

        print('Searching for player ' + str(player))
        await ctx.trigger_typing()

        try:
            URL = "http://live.albiononline.com/status.txt"
            a = requests.get(url = URL)
            data = a.json() #{ "status": "online", "message": "All good." }
            ctx.send('')
        except:
            ctx.send("Server connection timeout, there's propably a maintenance.")

def setup(client):
    client.add_cog(info(client))