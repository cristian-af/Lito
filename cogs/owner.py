from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import aiohttp

import datetime
from collections import Counter

import platform, pkg_resources

import copy
import os
from utils.settings import GREEN_EMBED, ERROR_EMOJI, SUCCESS_EMOJI, LOADING_EMOJI
import time, subprocess
from typing import Union

class Owner(commands.Cog):
    """Owner-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
        self.blocked = []
       
    async def cog_check(self, ctx):
        if not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner("You are not allowed to use this command.")
        return True

    @commands.command(name='load', hidden=False)
    async def _load(self, ctx, *, extension_name):
        """Loads a module."""
        try:
            wait = await ctx.send(f"<{LOADING_EMOJI}> Wait for some results.")
            await asyncio.sleep(1)
            await wait.delete()
            self.bot.load_extension(extension_name)
            await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")
        except Exception as e:
            await ctx.message.add_reaction(f"{ERROR_EMOJI}")
            await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")

    @commands.command(name='unload', hidden=False)
    async def _unload(self, ctx, *, extension_name):
        """Unloads a module."""
        try:
            wait = await ctx.send(f"Wait for some results.")
            await asyncio.sleep(1)
            await wait.delete()
            self.bot.unload_extension(extension_name)
            await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")
        except Exception as e:
            await ctx.message.add_reaction(f"{ERROR_EMOJI}")
            await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")

    @commands.command(name='reload', hidden=False)
    async def _reload(self, ctx, *, extension_name):
        """Reloads a module."""
        try:
            wait = await ctx.send(f"<{LOADING_EMOJI}> Wait for some results.")
            await asyncio.sleep(1)
            await wait.delete()
            self.bot.unload_extension(extension_name)
            self.bot.load_extension(extension_name)
            await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")
        except Exception as e:
            await ctx.message.add_reaction(f"{ERROR_EMOJI}")
            await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")
    

    @commands.group(hidden=True, name="activity")
    async def _activity(self, ctx):
        """A command that changes status playing and more."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Incorrect block subcommand passed.')

    @_activity.command()
    async def playing(self, ctx, *, activity: str):
        """Sets playing status in silent."""
        await self.bot.change_presence(activity=discord.Game(name=activity))
        await ctx.message.add_reaction(SUCCESS_EMOJI)


    @_activity.command()
    async def watching(self, ctx, *, activity: str):
        """Sets watching status in silent."""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        await ctx.message.add_reaction(SUCCESS_EMOJI)
    
    @_activity.command()
    async def listening(self, ctx, *, activity: str):
        """Sets listening status in silent."""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
        await ctx.message.add_reaction(SUCCESS_EMOJI)

    @_activity.command()
    async def streaming(self, ctx, url: str, *, activity: str):
        """Sets streaming status in silent."""
        await self.bot.change_presence(activity=discord.Streaming(name=activity, url=url))
        await ctx.message.add_reaction(SUCCESS_EMOJI)

    @commands.command(pass_context=True, aliases=["clc"])
    async def clearconsole(self, ctx):
        """Cleans up the console."""
        subprocess.run("clear")
        print(" ")
        print('Logged in as:')
        print('------')
        print(f'Username: {self.bot.user.name}')
        print(f'ID: {self.bot.user.id}')
        print(f'Active on: {len(self.bot.guilds)} Servers.')
        print(f'Users: {len(self.bot.users)}')
        print(f'Cogs loaded: {len(self.bot.cogs)}')
        print(f"OS version: {platform.system()}{platform.release()}")
        print(f"Python Version: {platform.python_version()}")
        print(f"discord.py version: {pkg_resources.get_distribution('discord.py').version}")
        print('------')
        subprocess.run(["pyfiglet","Lito"])
        print('------')
        await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")
        
              
    @commands.command()
    async def dm(self, ctx, member: discord.Member = None, *, text: str):
        user = self.bot.get_user(member.id)               
        await user.send(text)


def setup(bot):
    bot.add_cog(Owner(bot))
