import discord
from discord.ext import commands

import asyncio
import os
import platform, pkg_resources, subprocess, pyfiglet

import codecs
import os
import pathlib
import asyncpg

from utils.settings import GREEN_EMBED
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
from utils.settings import BOT_TOKEN, BOT_PREFIX

async def run():
    description = "A bot written in Python running on Android."

    credentials = {"user": "USERNAME", "password": "PASSWORD", "database": "DATABSE", "host": "127.0.0.1"}
    db = await asyncpg.create_pool(**credentials)

    bot = commands.Bot(description=description, db=db)
    bot.launch_time = datetime.utcnow()
    startup_extensions = ['cogs.owner','cogs.webhook','cogs.random','cogs.eh','jishaku']
    try:
        await bot.start(BOT_TOKEN)
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()

class Bot(commands.Bot):
    
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=commands.when_mentioned_or(BOT_PREFIX)
        )

        self.db = kwargs.pop("db")

    async def on_ready(self):
        print(" ")
        print('Logged in as:')
        print('------')
        print(f'Username: {self.bot.user.name}')
        print(f'ID: {self.bot.user.id}')
        print(f'Active on: {len(self.bot.guilds)} Servers.')
        print(f'Users: {len(self.bot.users)}')
        print(f'Cogs loaded: {len(self.bot.cogs)}')
        print('------')
        print(" ")
        subprocess.run(["figlet","Vito\nAndroid"])
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{BOT_PREFIX}help | {len(self.bot.users)} users."))

    @bot.command(name='stats')
    @commands.cooldown(1,5,BucketType.user) 
    async def _stats(ctx):
    """Shows the stats about the bot."""
        if ctx.author.bot:
            return
    
        total = 0
        file_amount = 0
        for path, subdirs, files in os.walk('.'):
            for name in files:
                if name.endswith('.py'):
                    file_amount += 1
                    with codecs.open('./' + str(pathlib.PurePath(path, name)), 'r', 'utf-8') as f:
                        for i, l in enumerate(f):
                            if l.strip().startswith('#') or len(l.strip()) is 0:
                                pass
                            else:
                                total += 1

    
        a1 = "``"
        a2 = "`"
        f = pyfiglet.Figlet(font='slant')
        f2 = f.renderText('Vito')
        delta_uptime = datetime.utcnow() - bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Stats"
        embed.description = f"{a1}{a2}{f2}{a1}{a2}\nPython Version: {platform.python_version()}\ndiscord.py version: {pkg_resources.get_distribution('discord.py').version}\nUsers: {len(bot.users)}\nPing latency: {round(bot.latency * 1000)}ms\nOwner: {bot.get_user(339752841612623872)}\nUptime: {days}d, {hours}h, {minutes}m, {seconds}s\nServers: {len(bot.guilds)}\nLine count: {total:,} lines and {file_amount:,} files."
        embed.set_footer(text=f"{bot.user.name}")
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

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
