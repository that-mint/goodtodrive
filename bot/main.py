import discord
from discord.ext import commands
import os
import re
import random
from random import choice

client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("GTDB | DM .help"))
    print("I am online")

# Auto add reactions when a certain word is said
# uses REGEX to check if its own word
# skips if the message is said by the bot itself. Can also make
# commands with the same name as the search, as the regex doesn't match
@client.listen('on_message')
async def whatever_you_want_to_call_it(message):
    if message.author == client.user:
        return
    elif re.search(r"(?i)\bpip\b", message.content):
        emoji = client.get_emoji(850738731274207262)
        await message.add_reaction(emoji)
    elif re.search(r"(?i)\bpipe\b", message.content):
        emoji = client.get_emoji(850738731274207262)
        await message.add_reaction(emoji)


# Auto add reactions to preexisting reactions
# Checks wether the reaction was added by the bot itself and skips
# Can work for any emote/emoji, just add it as its new client.get_emoji
@client.event
async def on_reaction_add(reaction, user):
    pip = client.get_emoji(850738731274207262)
    omegalul = client.get_emoji(365763491660824576)
    if user == client.user:
        return
    elif reaction.emoji == pip:
        await reaction.message.add_reaction(pip)
    elif reaction.emoji == omegalul:
        await reaction.message.add_reaction(omegalul)


# Command block, relatively self explanatory
@client.command(brief="Ping the bot",)
async def ping(ctx):
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 4))}")

@client.command(brief="Tests how good you are to drive", name="goodtodrive", aliases=["gtd"])
async def goodtodrive(ctx):
    determine_flip = [1, 0]
    if random.choice(determine_flip) == 1:
        await ctx.send(f"{ctx.message.author.mention} is good to drive! <:thepip:850738731274207262>🌿🏎️")

    else:
        await ctx.send(f" {ctx.message.author.mention} isn't good to drive :( <:thepip:850738731274207262>🌿💥👪🚔🚨")

@client.command(brief="Mentions the user who used the command", name="whoami")
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.mention}")

@client.command(brief="ADMIN: Clears the chat", name="clear")
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@client.command(brief="Links the source of the bot", name="source")
async def source(ctx):
    await ctx.send(f" {ctx.message.author.mention} https://github.com/that-mint/goodtodrive")

client.run(token)