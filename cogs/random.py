import discord
from discord.ext import commands

import asyncio
import os
import random
import aiohttp
import humanize
from datetime import datetime
from utils.settings import GREEN_EMBED, ERROR_EMOJI
import utils.checks
from discord.ext.commands.cooldowns import BucketType

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.check(utils.checks.is_bot)
    @commands.guild_only()
    async def random(self, ctx):
        """Chooses a random user."""
        
        user = random.choice(ctx.guild.members)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Random Member"
        embed.description = f"User: {self.bot.get_user(user.id)}\nUser ID: {user.id}\nBot: {user.bot}\nJoined At: {user.joined_at}"
        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def dadjoke(self, ctx):
        """Says a dad joke."""
        try:
            headers = {"Accept": "application/json"}
            async with aiohttp.ClientSession() as session:
                async with session.get('https://icanhazdadjoke.com', headers=headers) as get:
                    resp = await get.json()
                    embed = discord.Embed(color=GREEN_EMBED)
                    embed.title = "A dad joke."
                    embed.description = f"{resp['joke']}"
                    embed.set_footer(text=f"{self.bot.user.name}")
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"{e}")

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def userinfo(self, ctx, member: discord.Member):
        """Shows information about the user."""
        status = member.status
        
        if status == "online" or "<Status.online: 'online'>":
            status = f"{status} - <:status_online:596576749790429200>"
            pass
        if status == "idle" or "<Status.idle: 'idle'>":
            status = f"{status} - <:status_idle:596576773488115722>"
            pass
        if status == "dnd" or "<Status.dnd: 'dnd'>":
            status = f"{status} -  <:status_dnd:596576774364856321>"
            pass
        if status == "offline" or "<Status.offline: 'offline'>":
            status = f"{status} - <:status_offline:596576752013279242> "
            pass
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = f"{member}"
        embed.description = f"Status: {status}\nUser ID: ``{member.id}``\nBot: {member.bot}\nJoined: {humanize.naturaldate(member.joined_at)}\nCreated: {humanize.naturaldate(member.created_at)}\n```{member.activity}```"
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=member.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def guildinfo(self, ctx):
        """Shows information about the server."""
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = f"{ctx.guild.name} | {ctx.guild.id}"
        embed.description = f"Owner: {ctx.guild.owner.mention} | ID: {ctx.guild.owner.id}\nCreated: {humanize.naturaldate(ctx.guild.created_at)}\nIcon URL: [Click here]({ctx.guild.icon_url})" 
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,60,BucketType.guild)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def feedback(self, ctx, *, text: str):
        """A command that sends feedback."""
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Feedback"
        embed.description = f"A user named `{ctx.author.name}` sent a feedback that says:\n\n{text}"
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        await self.bot.get_channel(592424825675579412).send(embed=embed)
        await ctx.send(f"Thank you for your feedback, {ctx.author.name}. :ok_hand:")
    
    @commands.command()
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    @commands.cooldown(1.0, 30.0, commands.BucketType.user)
    async def hownonce(self, ctx, user: discord.Member = None):
        """How much of an nonce he is?"""
        if user is None:
            user = ctx.author
            random.seed(user.id)
            percent = random.randint(0, 100)
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = "How much of a nonce are you?"
            embed.description = f"You are {percent}% nonce."
            embed.set_footer(text=f"{self.bot.user.name}")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            random.seed(user.id)
            percent = random.randint(0, 100)
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = f"How much of an nonce is {user.name}?"
            embed.description = f"{user.mention} is {percent}% nonce."
            embed.set_footer(text=f"{self.bot.user.name}")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,60,BucketType.guild)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def takethenoose(self, ctx):
        """Just take the noose."""
        await ctx.send("aight.")

def setup(bot):
    bot.add_cog(Random(bot))
