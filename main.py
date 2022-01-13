import discord
from discord.ext import commands
import os
import re
import random
import asyncio
from random import choice
import mysql.connector as database
import sql
from decouple import config

client = commands.Bot(command_prefix=".")
token = config("DISCORD_BOT_TOKEN")

# Comment this to false to disable SQL/points connectivity. Currently broken if false
sqlenabled = True

blockedchannels = [887901232075788319]



@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("GTDB | DM .help"))
    print("I am online")

# skips if the message is said by the bot itself. Can also make
# commands with the same name as the search, as the regex doesn't match.
# Can be expanded upon to add any emoji to any word, just add a new elif.
@client.listen('on_message')
async def autoreact(message):
    if message.author == client.user:
        return
    elif message.channel.id in blockedchannels:
        return
    elif re.search(r"(?i)\bpip\b", message.content):
        emoji = client.get_emoji(850738731274207262)
        await message.add_reaction(emoji)
    elif re.search(r"(?i)\bpipe\b", message.content):
        emoji = client.get_emoji(850738731274207262)
        await message.add_reaction(emoji)


# Delete messages in the roles channel after a delay.
# Used with Auttaja for self-serviced roles.
@client.event
#async def on_message(message):
    #if message.channel.id == 928139023875211315:
        #await asyncio.sleep(5)
        #print("Deleted message in roles channel:")
        #print(message.content)
        #await message.delete()



# Auto add reactions to preexisting reactions
# Checks wether the reaction was added by the bot itself and skips
# Can work for any emote/emoji, just add it as its new client.get_emoji
@client.event
async def on_reaction_add(reaction, user):
    pip = client.get_emoji(850738731274207262)
    omegalul = client.get_emoji(365763491660824576)
    if user == client.user:
        return
    elif reaction.message.channel.id in blockedchannels:
        return
    elif reaction.emoji == pip:
        await reaction.message.add_reaction(pip)
    elif reaction.emoji == omegalul:
        await reaction.message.add_reaction(omegalul)


# Command block, relatively self explanatory
@client.command(brief="Ping the bot",)
async def ping(ctx):
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 4))}")
    if sqlenabled:
        sql.add_data(ctx.message.author.name, "ping")

@client.command(brief="Good to drive statistics",)
async def gtdstats(ctx):
    sql.add_data(ctx.message.author.name, "gtdstats")
    async with ctx.typing():
        await ctx.message.delete()
        embed=discord.Embed(title="Good To Drive Statistics", description="How fried is the server?", color=0x66ffb0)
        embed.set_author(name="Good to Drive", icon_url="https://i.imgur.com/c159g2g.png")
        embed.add_field(name="Total Deaths:", value=sql.get_data_command('gtdfail'), inline=False)
        embed.add_field(name="Total Saves:", value=sql.get_data_command('gtdpass'), inline=True)
        embed.set_footer(text="Good to drive, boss.")
        await ctx.send(embed=embed)


@client.command(brief="Tests how good you are to drive", name="goodtodrive", aliases=["gtd"])
async def goodtodrive(ctx):
    pip = client.get_emoji(850738731274207262)
    determine_flip = [1, 0]
    await ctx.message.delete()
    async with ctx.typing():
        if random.choice(determine_flip) == 1:
            sql.add_data(ctx.message.author.name, "gtdpass")
            m = await ctx.send(f"{ctx.message.author.mention} is good to drive, they have saved {sql.get_data('gtdpass',ctx.message.author.name)} families! <:thepip:850738731274207262>")
            await m.add_reaction(pip)
        else:
            sql.add_data(ctx.message.author.name, "gtdfail")
            m = await ctx.send(f" {ctx.message.author.mention} isn't good to drive, they have killed {sql.get_data('gtdfail',ctx.message.author.name)} families <:thepip:850738731274207262>")
            await m.add_reaction(pip)

@client.command(brief="Tally the deja beug counter", name="dejabeug", aliases=["db"])
async def dejabeug(ctx):
    beug = client.get_emoji(862251320264884225)
    await ctx.message.delete()
    async with ctx.typing():
        sql.add_data(ctx.message.author.name, "dejabeug")
        m = await ctx.send(f"{ctx.message.author.mention} has had deja beug, this is their {sql.ordinal(sql.get_data('dejabeug',ctx.message.author.name))} time! | {sql.get_data_command('dejabeug')} total deja beugs! <:thebeug:862251320264884225>")
        await m.add_reaction(beug)

@client.command(brief="deja beug leaderboard", name="dbl")
async def dbl(ctx):
    async with ctx.typing():
        await ctx.message.delete()
        sql.add_data(ctx.message.author.name, "dbl")
        alldata = sql.get_data_dbleaderboard()
        embed=discord.Embed(title="Deja Beug Leaderboard (Top 5)", description="Who has the most deja beugs!", color=0x66ffb0)
        embed.set_author(name="Good to Drive", icon_url="https://i.imgur.com/c159g2g.png")
        for row in alldata:
            embed.add_field(name=row[0], value=row[1], inline=False)
        await ctx.send(embed=embed)


@client.command(brief="Mentions the user who used the command", name="whoami")
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.mention}")
    if sqlenabled:
        sql.add_data(ctx.message.author.name, "mention")

@client.command(brief="ADMIN: Clears the chat", name="clear")
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@client.command(brief="Links the source of the bot", name="source")
async def source(ctx):
    await ctx.send(f" {ctx.message.author.mention} https://github.com/that-mint/goodtodrive")
    if sqlenabled:
        sql.add_data(ctx.message.author.name, "source")

client.run(token)

