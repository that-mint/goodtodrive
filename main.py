import discord
from discord.ext import commands
import os
import re
import random
from random import choice
import mysql.connector as database
from decouple import config

client = commands.Bot(command_prefix=".")
token = config("DISCORD_BOT_TOKEN")

# Comment this to false to disable SQL/points connectivity. Currently broken if false
sqlenabled = True

sqlhost = config("MYSQL_HOST")
sqluser = config("MYSQL_USER")
sqlpass = config("MYSQL_PASS")
sqldb = config("MYSQL_DB")


def add_data(nick, command):
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor(buffered=True)
    try:
        statement = "INSERT INTO points (nick,command) VALUES (%s, %s)"
        data = (nick, command)
        cursor.execute(statement, data)
        connection.commit()
        print(f"Successfully added entry to database with variables {nick} & {command}")
        connection.close()
    except database.Error as e:
        print(f"Error adding entry to database: {e}")
        connection.close()

CMDCOUNT = 0

def get_data(command,nick):
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor(buffered=True)
    try:
        sql = "SELECT COUNT(*) FROM points WHERE command = %s AND nick = %s"
        args = (command, nick)
        cursor.execute(sql, args)
        result=cursor.fetchone()
        number_of_rows = result[0]
        global CMDCOUNT
        CMDCOUNT = number_of_rows
        connection.close()
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        connection.close()

def get_data_command(command):
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor(buffered=True)
    try:
        sql = "SELECT COUNT(*) FROM points WHERE command = %s"
        args = (command,)
        cursor.execute(sql, args)
        result=cursor.fetchone()
        number_of_rows = result[0]
        global CMDCOUNT
        CMDCOUNT = number_of_rows
        connection.close()
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        connection.close()

def ordinal(n):
  s = ('th', 'st', 'nd', 'rd') + ('th',)*10
  v = n%100
  if v > 13:
    return f'{n}{s[v%10]}'
  else:
    return f'{n}{s[v]}'

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("GTDB | DM .help"))
    print("I am online")

# Auto add reactions when a certain word is said
# uses REGEX to check if its own word
# skips if the message is said by the bot itself. Can also make
# commands with the same name as the search, as the regex doesn't match.
# Can be expanded upon to add any emoji to any word, just add a new elif.
@client.listen('on_message')
async def autoreact(message):
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
    if sqlenabled:
        add_data(ctx.message.author.name, "ping")

@client.command(brief="Good to drive statistics",)
async def gtdstats(ctx):
    add_data(ctx.message.author.name, "gtdstats")
    async with ctx.typing():
        get_data_command("gtdpass")
        passtotal = CMDCOUNT
        get_data_command("gtdfail")
        failtotal = CMDCOUNT
        await ctx.message.delete()
        embed=discord.Embed(title="Good To Drive Statistics", description="How fried is the server?", color=0x66ffb0)
        embed.set_author(name="Good to Drive", icon_url="https://i.imgur.com/c159g2g.png")
        embed.add_field(name="Total Deaths:", value=passtotal, inline=False)
        embed.add_field(name="Total Saves:", value=failtotal, inline=True)
        embed.set_footer(text="Good to drive, boss.")
        await ctx.send(embed=embed)


@client.command(brief="Tests how good you are to drive", name="goodtodrive", aliases=["gtd"])
async def goodtodrive(ctx):
    pip = client.get_emoji(850738731274207262)
    determine_flip = [1, 0]
    await ctx.message.delete()
    async with ctx.typing():
        if random.choice(determine_flip) == 1:
            add_data(ctx.message.author.name, "gtdpass")
            get_data("gtdpass",ctx.message.author.name)
            m = await ctx.send(f"{ctx.message.author.mention} is good to drive, they have saved {CMDCOUNT} families! <:thepip:850738731274207262>")
            await m.add_reaction(pip)
        else:
            add_data(ctx.message.author.name, "gtdfail")
            get_data("gtdfail",ctx.message.author.name)
            m = await ctx.send(f" {ctx.message.author.mention} isn't good to drive, they have killed {CMDCOUNT} families <:thepip:850738731274207262>")
            await m.add_reaction(pip)

@client.command(brief="Tally the deja beug counter", name="dejabeug", aliases=["db"])
async def dejabeug(ctx):
    beug = client.get_emoji(862251320264884225)
    await ctx.message.delete()
    async with ctx.typing():
        add_data(ctx.message.author.name, "dejabeug")
        get_data_command("dejabeug")
        dejatotal = CMDCOUNT
        get_data("dejabeug",ctx.message.author.name)
        usertotal = CMDCOUNT
        ordinal(usertotal) = usertotal
        m = await ctx.send(f"{ctx.message.author.mention} has had deja beug, this is their {usertotal} time! | {dejatotal} total deja beugs! <:thebeug:862251320264884225>")
        await m.add_reaction(beug)


@client.command(brief="Mentions the user who used the command", name="whoami")
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.mention}")
    if sqlenabled:
        add_data(ctx.message.author.name, "mention")

@client.command(brief="ADMIN: Clears the chat", name="clear")
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@client.command(brief="Links the source of the bot", name="source")
async def source(ctx):
    await ctx.send(f" {ctx.message.author.mention} https://github.com/that-mint/goodtodrive")
    if sqlenabled:
        add_data(ctx.message.author.name, "source")

client.run(token)
