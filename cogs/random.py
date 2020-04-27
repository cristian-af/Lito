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
        """Chooses a random user. 5 second cooldown."""
        
        user = random.choice(ctx.guild.members)
        test = self.bot.get_user(user.id)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.description = f"User ID: {user.id}\nBot: {user.bot}\nJoined At: {humanize.naturaldate(user.joined_at)}\nStatus: {user.status}\n```{user.activity}```"
        embed.set_footer(text=test)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,2,BucketType.user)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def dadjoke(self, ctx):
        """Says a dad joke. 2 second cooldown."""
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
    async def userinfo(self, ctx, member: discord.Member = None):
        """Shows information about the user. 5 second cooldown."""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = f"{member}"
        embed.description = f"Status: {member.status}\nUser ID: ``{member.id}``\nBot: {member.bot}\nJoined: {humanize.naturaldate(member.joined_at)}\nCreated: {humanize.naturaldate(member.created_at)}\n```{member.activity}```"
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=member.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def guildinfo(self, ctx):
        """Shows information about the server. 5 second cooldown."""
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = f"{ctx.guild.name}"
        embed.description = f"Users: {len(ctx.guild.members)}\nID: {ctx.guild.id}\nCreated: {humanize.naturaldate(ctx.guild.created_at)}\nIcon URL: [Click here]({ctx.guild.icon_url})\nBoosts & Tier: {ctx.guild.premium_subscription_count} - Tier {ctx.guild.premium_tier}" 
        embed.set_footer(text=f"{ctx.guild.owner} | {ctx.guild.owner.id}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,150,BucketType.user)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    async def feedback(self, ctx, *, text: str):
        """A command that sends feedback to the owner. 150 second cooldown"""
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Feedback"
        embed.description = f"A user named `{ctx.author}` with the id `{ctx.author.id}` from `{ctx.guild}` sent feedback that says:\n\n```{text}```"
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        await self.bot.get_channel(592424825675579412).send(embed=embed)
        response = discord.Embed(color=GREEN_EMBED)
        response.title = "Thank you!"
        response.description = "I highly appreciate the feedback that is sent to make a suggestion or a bug report or just feedback on how good the bot is! Thank you!"
        response.set_footer(text=self.bot.user.name)                           
        await ctx.send(embed=response)
    
    
    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, member: discord.Member = None, *, text: str):
        """DMs a user.. Owner only."""
        user = self.bot.get_user(member.id)               
        await user.send(text)
    
    @commands.command()
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    @commands.cooldown(4.0, 2, commands.BucketType.user)
    async def hownonce(self, ctx, user: discord.Member = None):
        """How much of an nonce he is? 2 second cooldown with 4 tries."""
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
            
    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(utils.checks.is_bot)
    @commands.cooldown(4.0, 2, commands.BucketType.user)
    async def secretcommando(self, ctx, user: discord.Member = None):
        """Do not explain why. I was forced. 2 second cooldown with 4 tries."""
        if user is None:
            user = ctx.author
        server = self.bot.get_guild(336642139381301249).members
        if ctx.author in server:
           random.seed(user.id)
           dong = f"8" + "="*random.randint(0, 30) + "D"
           embed = discord.Embed(color=GREEN_EMBED)
           embed.description = f"{user.name}'s dong size.\n{dong}"
           return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Random(bot))
