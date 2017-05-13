#!/usr/bin/env python3
import discord
import re
from discord.ext import commands
import asyncio
import nltk
import random
import logging
from Bot import Bot
import requests

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)
#client = discord.Client()
client = commands.Bot(command_prefix="!")

@client.event
@asyncio.coroutine
def on_ready():
    logging.info("Logged in as %s" % client.user.name)
    with open('game.txt') as f:
        game = f.read()
    yield from client.change_status(discord.Game(name=game))

@client.event
@asyncio.coroutine
def on_message(message):
    logging.info("Received message: %s" % message.content)
    if message.author == client.user:
        logging.info("Skipping (message from client)")
        return
    logging.info("Checking if we should reply...")
    p = re.compile(r'(?<!gnu/)(?<!gnu plus )linux', re.IGNORECASE)
    if p.search(message.content):
        msg = """I'd just like to interject for a moment.  What you're referring to as Linux,
is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux.
Linux is not an operating system unto itself, but rather another free component
of a fully functioning GNU system made useful by the GNU corelibs, shell
utilities and vital system components comprising a full OS as defined by POSIX.

Many computer users run a modified version of the GNU system every day,
without realizing it.  Through a peculiar turn of events, the version of GNU
which is widely used today is often called "Linux", and many of its users are
not aware that it is basically the GNU system, developed by the GNU Project.

There really is a Linux, and these people are using it, but it is just a
part of the system they use.  Linux is the kernel: the program in the system
that allocates the machine's resources to the other programs that you run.
The kernel is an essential part of an operating system, but useless by itself;
it can only function in the context of a complete operating system.  Linux is
normally used in combination with the GNU operating system: the whole system
is basically GNU with Linux added, or GNU/Linux.  All the so-called "Linux"
distributions are really distributions of GNU/Linux."""
    else:
        msg = yield from cuck_message(message.content)
    if msg:
        logging.info("Posting reply: %s" % msg)
        yield from client.send_message(message.channel, msg)
    else:
        logging.info("No.")
    yield from client.process_commands(message)

@client.command()
@asyncio.coroutine
def bplay(game):
    if game.lower().strip() == "linux":
        game = "GNU/Linux"
    with open('game.txt', 'w') as f:
        f.write(game)
    yield from client.change_status(discord.Game(name=game))

@client.command()
@asyncio.coroutine
def bfaq(query):
    if query.lower() == "overwatch":
        yield from client.say("Overwatch is a bad game")
        return
    url = 'http://api.duckduckgo.com/?q={}&format=json&pretty=1'.format(query)
    r = requests.get(url)
    r.raise_for_status()
    j = r.json()
    try:
        a = j['AbstractText']
        b = j['AbstractURL']
        if a:
            yield from client.say(a)
        elif b:
            yield from client.say(b)
        else:
            yield from client.say("idk")
    except:
        yield from client.say("idk")

@client.command()
@asyncio.coroutine
def yw(sa, *args):
    msg = ""
    if sa == "newtopic":
        b = Bot()
        b.login('b', '123456')
        subject = args[0]
        message = args[1]
        msg = b.new_topic("8", subject, message)
    elif sa == "getrecent":
        b = Bot()
        b.login('b', '123456')
        msg = "\n".join(str(r) for r in b.get_recent())
    elif sa == "ratepost":
        b = Bot()
        b.login('b', '123456')
        b.rate_post(args[0], args[1])
        msg = args[0]
    if msg:
        yield from client.say(msg)
        

@asyncio.coroutine
def cuck_message(message):
    always_cuck = "!cuck" in message
    if always_cuck:
        message = message.replace("!cuck", "").strip()
    tokens = nltk.word_tokenize(message)
    tagged = nltk.pos_tag(tokens)
    nouns = []
    for word, tag in tagged:
        if tag.startswith('N'):
            nouns.append(word)
    if nouns and always_cuck or random.random() < .02:
        choice = random.choice(nouns)
        message = message.replace(choice, "cuck")
        return message

if __name__ == "__main__":
    client.run('YOUR_TOKEN_HERE')
