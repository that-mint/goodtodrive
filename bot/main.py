import discord
from discord.ext import commands
import os

import random
from random import choice

client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("GTDB | DM .help"))
    print("I am online")

@client.event
async def on_message(message):
    # we do not want the client to reply to itself
    if message.author == client.user:
        return
    if "PIP" in message.content or "pip" in message.content:
        emoji = client.get_emoji(850738731274207262)
        await message.add_reaction(message, emoji)
    elif:
        await client.process_commands(message)

@client.command(brief="Ping the bot",)
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(brief="Tests how good you are to drive", name="goodtodrive", aliases=["gtd"])
async def goodtodrive(ctx) :
    determine_flip = [1, 0]
    if random.choice(determine_flip) == 1:
        await ctx.send(f"{ctx.message.author.mention} is good to drive! <:thepip:850738731274207262>🌿🏎️")

    else:
        await ctx.send(f" {ctx.message.author.mention} isn't good to drive :( <:thepip:850738731274207262>🌿💥👪🚔🚨")

@client.command(brief="Mentions the user who used the command", name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.mention}")

@client.command(brief="ADMIN: Clears the chat", name="clear")
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

@client.command(brief="Links the source of the bot", name="source")
async def source(ctx) :
    await ctx.send(f" {ctx.message.author.mention} https://github.com/that-mint/goodtodrive")

client.run(token)