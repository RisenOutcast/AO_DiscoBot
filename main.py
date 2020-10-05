import discord
import random
import asyncio
import json
import socket
import requests
import os
from os.path import isfile, join
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands
from pathlib import Path


print("Current Computer:\n" + str(socket.gethostname()))
running_on = socket.gethostname()

TOKEN = open("token.txt","r").read()

Metso = 255801554311839764

with open("prefixes.json") as f:
    prefixes = json.load(f)
default_prefix = "?"

def prefix(bot, message):
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)
    id = str(message.guild.id)
    if not id in prefixes:
        prefixes[id] = default_prefix 
        with open("prefixes.json", 'w') as f:
            json.dump(prefixes, f)
    return prefixes.get(id, default_prefix)

client = Bot(command_prefix=prefix)

client.remove_command('help')
goldvalue = 0
servers = []

async def change_status():
    await client.wait_until_ready()
    status = ['type ?help', 'author@RisenOutcast']

    while not client.is_closed():
        await client.change_presence(activity=discord.Game(name=random.choice(status)))
        await asyncio.sleep(60)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print(client.user.id)
    print('------')
    for guild in client.guilds:
        servers.append(guild.name)

    if not hasattr(client, 'AppInfo'):
        client.AppInfo = await client.application_info()

@client.command(pass_context=True)
async def prefixchange(ctx, newprefix):
    if ctx.message.author.guild_permissions.kick_members:
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)
        id = str(ctx.message.guild.id)
        if newprefix == None:
            ctx.send('There was no new prefix given! ``?prefixchange ~newprefix~``')
        prefixes[id] = newprefix 
        with open("prefixes.json", 'w') as f:
            json.dump(prefixes, f)
        await ctx.send('Prefix changed to `{}`'.format(newprefix))
    else:
        await ctx.send('Only server admin has permission to change servers prefix!')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.author.id == 456597569959624705:
        return
    if message.author.bot:
        return
    
    if client.user.mentioned_in(message) and message.mention_everyone is False:
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)
        id = str(message.guild.id)
        await message.channel.send("Current prefix for this server is `{}`".format(prefixes[id]))

    await client.process_commands(message)


#@client.command(pass_context=True)
#async def role(ctx, rooli):
    #user = ctx.message.author
    #if ctx.message.guild.id == '523422493151592458' or '444946819492085760':
        #if rooli not in ctx.message.author.roles:
            #if rooli in Appointable:
                #role = discord.utils.get(ctx.guild.roles, name=rooli)
                #if role in user.roles:
                    #await ctx.message.author.remove_roles(role)
                    #await ctx.send('Role **{}** has been removed from you!'.format(rooli))
                #else:
                    #await ctx.message.author.add_roles(role)
                    #await ctx.send('You now have **{}** as a role'.format(rooli))
            #else:
                #await ctx.send("Role isn't self appointable or doesn't exist!")
        #else:
            #await ctx.send("Role doesn't exist")
    #else:
        #await ctx.send('Command not configured for this server.')

@client.command(pass_context=True, aliases=['Help'])
async def help(ctx):
    embed = discord.Embed(
    colour = discord.Colour.blue(),
    )
    embed.set_author(name='Commandlist ({}~commandname~)'.format(prefix))
    embed.add_field(name='Gold', value='See the current price of 1 gold', inline=False)
    embed.add_field(name='Price ~item~', value='Items value in different cities', inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=['Gold'])
async def gold(ctx):
    URL = "https://www.albion-online-data.com/api/v2/stats/gold?count=1"
    #Parameters = {'price':}

    #[{"price":2838,"timestamp":"2020-07-10T00:00:00"}]

    a = requests.get(url = URL)
    data = a.json()

    print(data[0]['price'])
    goldvalue = data[0]['price']
    await ctx.send("1 gold is worth {} silver!".format(goldvalue))
    
@client.command(pass_context=True, aliases=['Data'])
async def data(ctx):
    if ctx.message.author.id == Metso:
        with open("index.json", 'r') as f:
            index = json.load(f)
        #THE ALBION ONLINE DATA PROJECT's item data list
        URL = "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json"
        a = requests.get(url = URL)
        data = a.json()
        indexlist = data
        #Dump the data in a file
        with open("index.json", 'w') as f:
            json.dump(indexlist, f, sort_keys=True, indent=4)
        print('Index file done!')

        #The max amount of elements in the list
        Maxvalue = len(indexlist)
        print(Maxvalue)
        with open("index.json", 'r') as f:
            items = json.load(f)
        with open("items.json", 'r') as f:
            newlist = json.load(f)
        number = 0

        #Go through every single item and make a file with their name and id name UniqueName
        while number < int(Maxvalue):
            try:
                print(str(number) + ' ' + str(items[number]['LocalizedNames']['EN-US']))
                newlist[str(items[number]['LocalizedNames']['EN-US']).lower().replace("'", '')] = {}
                newlist[str(items[number]['LocalizedNames']['EN-US']).lower().replace("'", '')]['id'] = str(items[number]['UniqueName'])
                newlist[str(items[number]['LocalizedNames']['EN-US']).lower().replace("'", '')]['name'] = str(items[number]['LocalizedNames']['EN-US'])
                number += 1
            except:
                number += 1
                print(str(number) + ' failed')
        with open("items.json", 'w') as f:
            json.dump(newlist, f, sort_keys=True, indent=4)
        print('Itemlist done!')
    else:
        pass

@client.command(pass_context=True,aliases=['Price'])
async def price(ctx, quality, *, item : str = None):
    await ctx.trigger_typing()
    with open("items.json", 'r') as f:
        items = json.load(f)
    item_id = 0
    finalstr = item.replace("'", "")
    finalstr = finalstr.replace("´", "")
    finalstr = finalstr.replace("`", "")
    finalstr = finalstr.lower()
    #print(finalstr)
    try:
        if finalstr in items:
            #print(items[finalstr]['id'])
            item_id = items[finalstr]['id']
    except:
        pass
    
    URL = 'https://www.albion-online-data.com/api/v2/stats/prices/{}'.format(item_id)
    locations = 'Caerleon,Bridgewatch,FortSterling,Thetford,Lymhurst,Martlock,BlackMarket,ArthursRest,MorganasRest,MarlynsRest'
    qualities = '1,2,3,4,5,6'
    if quality in qualities:
        PARAMS = {'locations':locations,'qualities':quality}
    else:
        PARAMS = {'locations':locations,'qualities':qualities}
    a = requests.get(url = URL, params=PARAMS)
    data = a.json()
    number = 0
    finalprices = {}

    finalprices['Caerleon'] = 'No Data'
    finalprices['Bridgewatch'] = 'No Data'
    finalprices['Fort Sterling'] = 'No Data'
    finalprices['Thetford'] = 'No Data'
    finalprices['Lymhurst'] = 'No Data'
    finalprices['Martlock'] = 'No Data'
    finalprices['Arthurs Rest'] = 'No Data'
    finalprices['Morganas Rest'] = 'No Data'
    finalprices['Marlyns Rest'] = 'No Data'

    try:
        print(items[finalstr]['name'])
    except:
        await ctx.send('Invalid item name!')
        return

    #Create a embed
    embed = discord.Embed(
    colour = discord.Colour.red(),
    )

    try:
        while number < 500:
            if data[number]['sell_price_min'] is not 0:
                average = int(((data[number]['sell_price_min'] + data[number]['buy_price_max']) / 2))
                finalprices['{}'.format(data[number]['city'])] = (' Min: **' + ((str(data[number]['sell_price_min']) + '** Max: **' + str(data[number]['buy_price_max']))) + '** Average: **' + str(average) + '**' ) 
                    #embed.add_field(name=data[number]['city'], value=average, inline=True)
                print(str(data[number]['city']) + ' Min Sell: ' + str(data[number]['sell_price_min']) + ' Max Sell: ' + str(data[number]['sell_price_max']) + ' Average ' + str(average))
                print(str(data[number]['city']) + ' Min Buy: ' + str(data[number]['buy_price_min']) + ' Max Buy: ' + str(data[number]['buy_price_max']) + ' Average ' + str(average)) 
                number +=1
            else:
                number +=1
    except:
        pass
    print(finalprices.values())
    print(sorted(finalprices))

    print(finalprices)
    print('**Thetford** : ' +   str(finalprices['Thetford']))

    #string = '**Arthurs Rest**:' + str(finalprices['Arthurs Rest']) + '\n' + '**Bridgewatch**:' + str(finalprices['Bridgewatch']) + '\n' + '**Carleon**: ' + str(finalprices['Caerleon']) + '\n' + '**Fort Sterling**: ' + str(finalprices['Fort Sterling']) + '\n' + '**Lymhurst**: ' + str(finalprices['Lymhurst']) + '\n'

    Locationsstring = '**Arthurs Rest**:' + '\n' + '**Bridgewatch**:' + '\n' + '**Carleon**: ' + '\n' + '**Fort Sterling**: ' + '\n' + '**Lymhurst**: ' + '\n' '**Marlyns Rest**: ' + '\n' + '**Martlock**: ' + '\n' + '**Morganas Rest**: ' + '\n' '**Thetford**: '
    string = str(finalprices['Arthurs Rest']) + '\n' +  str(finalprices['Bridgewatch']) + '\n' +  str(finalprices['Caerleon']) + '\n'  + str(finalprices['Fort Sterling']) + '\n' +  str(finalprices['Lymhurst']) + '\n' + str(finalprices['Marlyns Rest']) + '\n' + str(finalprices['Martlock']) + '\n' + str(finalprices['Morganas Rest']) + '\n' + str(finalprices['Thetford']) + '\n'


    embed.add_field(name='Locations', value=Locationsstring, inline=True)
    embed.add_field(name='Prices (Min sell, Max buy, Average)', value=string, inline=True)

    embed.set_author(name=items[finalstr]['name'])

    #let's get the image too!
    embed.set_thumbnail(url="https://albiononline2d.ams3.cdn.digitaloceanspaces.com/thumbnails/orig/{}".format(item_id))
    await ctx.send(embed=embed)
    
@client.command(pass_context=True, aliases=['restart'], hidden=True)
async def shutdown(ctx):
    if ctx.message.author.id == Metso:
        await ctx.send("Shutting down....")
        await client.logout()
    else:
        await ctx.send("You have no power over me!")

async def list_servers():
    membercount = 0
    await client.wait_until_ready()
    while not client.is_closed():
        membercount = 0
        print('------')
        print("Current servers:")
        for guild in client.guilds:
            print(guild.name)
        print('------')
        for guild in client.guilds:
            for member in guild.members:
                if str(member.status) == 'online':
                    membercount += 1
                elif str(member.status) == 'idle':
                    membercount += 1
                elif str(member.status) == 'offline':
                    membercount += 1
        print("Current usercount: " + str(membercount))
        print('------')
        await asyncio.sleep(18000)





if __name__ == '__main__':
    cogs_dir = "cogs"
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            client.load_extension(cogs_dir + "." + extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

client.loop.create_task(list_servers())
client.loop.create_task(change_status())
client.run(TOKEN)