import discord
from discord.ext import commands

import asyncio
import os
import platform, pkg_resources, subprocess, pyfiglet
import codecs, humanize

from utils.settings import BOT_TOKEN, BOT_PREFIX
import utils.checks
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
import logging

description = "If you want to check the source just use the command [source]."

def get_prefix(bot, message):
    prefixes = ['Lito ', 'lito ', 'LITO ']

    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(description=description, command_prefix=get_prefix)
bot.launch_time = datetime.utcnow()
startup_extensions = ['cogs.owner','cogs.webhook','cogs.random','cogs.eh','jishaku']

@bot.event
async def on_ready():
    subprocess.run(["pyfiglet","Lito"])
    print(" ")
    print(f"Logged in as {bot.user.name} (ID {bot.user.id}), {bot.user.name} is in {len(bot.guilds)} servers and sees {len(bot.users)} users.")
    print(f"{len(bot.cogs)} cogs loaded, running on discord.py version {pkg_resources.get_distribution('discord.py').version}.")
    print(f"Python version is {platform.python_version()} and running on {platform.system()}{platform.release()}.")
          
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{BOT_PREFIX}help | {len(bot.users)} users."))
                                                       
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)     
          
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(BOT_TOKEN)
