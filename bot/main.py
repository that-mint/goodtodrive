import discord
from discord.ext import commands
import os
import re
import random
from random import choice
import mysql.connector as database

client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")

# Comment this to false to disable SQL/points connectivity.
sqlenabled = True

sqlhost = os.getenv("MYSQL_HOST")
sqluser = os.getenv("MYSQL_USER")
sqlpass = os.getenv("MYSQL_PASS")
sqldb = os.getenv("MYSQL_DB")

if sqlenabled:
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor()

def add_data(nick, command):
    try:
        statement = "INSERT INTO points (nick,command) VALUES (%s, %s)"
        data = (nick, command)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")

cmdcount = 0

def get_data(command,nick):
    try:
        sql = "SELECT COUNT(*) FROM points WHERE command = %s AND nick = %s"
        args = (command, nick)
        cursor.execute(sql, args)
        result=cursor.fetchone()
        number_of_rows = result[0]
        global cmdcount
        cmdcount = number_of_rows
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")

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


@client.command(brief="Tests how good you are to drive", name="goodtodrive", aliases=["gtd"])
async def goodtodrive(ctx):
    pip = client.get_emoji(850738731274207262)
    determine_flip = [1, 0]
    await ctx.message.delete()
    if random.choice(determine_flip) == 1:
        get_data("gtdpass",ctx.message.author.name)
        m = await ctx.send(f"{ctx.message.author.mention} is good to drive! <:thepip:850738731274207262>🌿🏎️ Count: {cmdcount}")
        await m.add_reaction(pip)
        if sqlenabled:
            add_data(ctx.message.author.name, "gtdpass")

    else:
       m = await ctx.send(f" {ctx.message.author.mention} isn't good to drive :( <:thepip:850738731274207262>🌿💥👪🚔🚨")
       await m.add_reaction(pip)
       if sqlenabled:
            add_data(ctx.message.author.name, "gtdfail")

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
connection.close()