import discord
from discord.ext import commands

import asyncio
import os
import random
import aiohttp
import humanize
from datetime import datetime
from utils.settings import GREEN_EMBED, ERROR_EMOJI
from discord.ext.commands.cooldowns import BucketType

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def random(self, ctx):
        """Chooses a random user."""
        if ctx.author.bot:
            return
        
        user = random.choice(ctx.guild.members)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Random Member"
        embed.description = f"User: {self.bot.get_user(user.id)}\n\nUser ID: {user.id}\n\nBot: {user.bot}\n\nJoined At: {user.joined_at}"
        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def dadjoke(self, ctx):
        """Says a dad joke."""
        if ctx.author.bot:
            return
        
        try:

            headers = {"Accept": "application/json"}

            async with aiohttp.ClientSession() as session:
                async with session.get('https://icanhazdadjoke.com', headers=headers) as get:
                    resp = await get.json()
                    await ctx.send(f"{resp['joke']}")
        except Exception as e:
            await ctx.send(f"{e}")

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member):
        """Shows information about the user."""
        if ctx.author.bot:
            return
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = f"{member}"
        embed.description = f"User ID: {member.id}\n\nBot: {member.bot}\n\nJoined: {humanize.naturaldate(member.joined_at)}\n\nCreated: {humanize.naturaldate(member.created_at)}"
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=member.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def guildinfo(self, ctx):
        """Shows information about the server."""
        if ctx.author.bot:
            return
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = f"{ctx.guild.name} | {ctx.guild.id}"
        embed.description = f"Owner: {ctx.guild.owner.mention} | ID: {ctx.guild.owner.id}\n\nCreated: {humanize.naturaldate(ctx.guild.created_at)}\n\nIcon URL: [Click here]({ctx.guild.icon_url})" 
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))
