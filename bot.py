import discord
from discord.ext import commands

import asyncio
import os
import platform, pkg_resources, subprocess, pyfiglet, psutil
import codecs, humanize
import pathlib

from utils.settings import GREEN_EMBED, BOT_TOKEN, BOT_PREFIX
import utils.checks
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
description = "I am a personal bot on a 7 android Huawei/android 5 Lenovo that runs on Termux which is a app on android.\nThere is no invite link, so don't bother to search for one, just no. If you want to check the source just use the command [source]."

def get_prefix(bot, message):
    prefixes = ['Lito ', 'lito ', 'LITO ']

    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(description=description, command_prefix=get_prefix)
bot.launch_time = datetime.utcnow()
startup_extensions = ['cogs.owner','cogs.webhook','cogs.random','cogs.eh','jishaku']

@bot.event
async def on_ready():
    print(" ")
    print('Logged in as:')
    print('------')
    print(f'Username: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(f'Active on: {len(bot.guilds)} Servers.')
    print(f'Users: {len(bot.users)}')
    print(f'Cogs loaded: {len(bot.cogs)}')
    print(f"OS version: {platform.system()}{platform.release()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"discord.py version: {pkg_resources.get_distribution('discord.py').version}")
    print('------')
    print(' ')
    subprocess.run(["pyfiglet","Lito"])
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{BOT_PREFIX}help | {len(bot.users)} users."))

@bot.command(name='stats', aliases=["info"])
@commands.check(utils.checks.is_bot)
@commands.cooldown(1,5,BucketType.user) 
async def _stats(ctx):
    """Shows the stats about the bot. 5 second cooldown."""
    total = 0
    file_amount = 0
    for path, subdirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.py'):
                file_amount += 1
                with codecs.open('./' + str(pathlib.PurePath(path, name)), 'r', 'utf-8') as f:
                    for i, l in enumerate(f):
                        if l.strip().startswith('#') or len(l.strip()) == 0:
                            pass
                        else:
                            total += 1
    test = "Termux"
    if platform.platform() == "Linux-3.10.65+-aarch64-with-glibc2.17":
          test = "Arch Linux ARM aarch64"
    else:
          test = "Termux"
    delta_uptime = datetime.utcnow() - bot.launch_time
    owner = bot.get_user(339752841612623872)
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(color=GREEN_EMBED)
    embed.title = "Stats"
    embed.add_field(name=f"Owned by {owner}", value=f"User ID: `{owner.id}`\nAccount created: `{humanize.naturaldate(owner.created_at)}`", inline=True)
    embed.description = f"OS: `{test}`\nOS kernel: `{platform.system()} {platform.release()}`\nOS booted since: `{datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}`\nPython Version: `{platform.python_version()}`\ndiscord.py version: `{pkg_resources.get_distribution('discord.py').version}`\n\nUsers: `{len(bot.users)}`\nPing latency: `{round(bot.latency * 1000)}ms`\n\nUptime: `{days}d, {hours}h, {minutes}m, {seconds}s`\nServers: `{len(bot.guilds)}`\nLine count: `{total:,} lines and {file_amount:,} files.`\n\nCPU Usage: `{psutil.cpu_percent()}%`\nVirtual Memory: `{humanize.naturalsize(psutil.virtual_memory().used)} ({psutil.virtual_memory().percent}%)`\nSwap memory: `{humanize.naturalsize(psutil.swap_memory().used)} - ({psutil.swap_memory().percent}%)`"
    embed.set_footer(text=bot.user.name)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)                                                         
     
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(BOT_TOKEN)
