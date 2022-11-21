

# bot.py
import os

import ShippingCalc
import discord
import asyncio
import json

from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
guild_id = os.getenv('guild_id')
logs_channel = os.getenv('logs_channel')


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            print(f"We have logged in as {self.user}.")


client =    aclient()

tree = app_commands.CommandTree(client)

@tree.command(name = "shipping",description = "Cssbuy Shipping Estimates für eingegebenes Gewicht")
async def self(interaction: discord.Interaction, weight:float):
    shippingChannelID = 781135941560565770
    texta = "dieser Graph dient lediglich zur Abschätzung der Versandkosten. Die Versandmethoden werden ohne Fees oder möglichen Volumenrestriktionen (mit (V) markiert) dargestellt  (siehe <#" + str(shippingChannelID) + "> -> Reiter Versandmethoden).\n\n"
    if(weight > 20000.0):
        weight = 20000.0
    if(weight < 0.0):
        weight = 0.0
    textb = "Kosten für **" + str(int(weight)) + "** Gramm:\n" 
    
    text = ShippingCalc.getPlotandPrices(weight)
    
    
    with open('ShippingPlot.png', 'rb') as f:
        picture = discord.File(f)
        userID = interaction.user.id

        
        await interaction.response.send_message("<@" + str(userID) + ">, "  + texta + textb + text,file=picture)


invites = {}
last = ""


@tasks.loop(seconds=4)
async def fetch():
    print("I am on!")
    global last
    global invites
    await client.wait_until_ready()
    gld = client.get_guild(int(guild_id))
    logs = client.get_channel(int(logs_channel))
    while True:
        
        invs = await gld.invites()
        tmp = []
        for i in invs:
            for s in invites:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        usr = gld.get_member(int(last))
                        eme = discord.Embed(description="Just joined the server", color=0x03d692, title=" ")
                        eme.set_author(name=usr.name + "#" + usr.discriminator, icon_url=usr.display_avatar)
                        eme.timestamp = usr.joined_at
                        date = usr.created_at
                        AccountOld= datetime.datetime.now() - date.replace(tzinfo=None)
                        warning = ""
                        if AccountOld.days <=31:
                            warning= "\n**ACCOUNT MADE LESS THAN A MONTH AGO**"
                        eme.add_field(name="Used invite",
                                      value="Inviter: " + i.inviter.mention + "\nUser: <@" + str(usr.id)+ ">\nAccount created on: " + str(usr.created_at)[:10]   + "\nUses: `" + str(
                                          i.uses) + "`" + warning  , inline=False)
                        await logs.send(embed=eme)
            tmp.append(tuple((i.code, i.uses)))
        invites = tmp
        


@client.event
async def on_ready():
    print("ready!")
    fetch.start()
    await client.change_presence(activity=discord.Activity(name="joins", type=2))


@client.event
async def on_member_join(meme):
    global last
    last = str(meme.id)


client.run(TOKEN)

