import discord
from discord.ext import commands
import os

import random
from random import choice

client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready() :
    await client.change_presence(activity = discord.Game("GTDB | .help"))
    print("I am online")

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="goodtodrive", aliases=["gtd"])
async def goodtodrive(ctx) :
    determine_flip = [1, 0]
    if random.choice(determine_flip) == 1:
        await ctx.send(f"{ctx.message.author.mention} is good to drive! <:thepip:850738731274207262>🌿🏎️")

    else:
        await ctx.send(f" {ctx.message.author.mention} isn't good to drive :( <:thepip:850738731274207262>🌿💥👪🚔🚨")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.mention}")

@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

client.run(token)