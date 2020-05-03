import discord
from discord.ext import commands

import asyncio
import os
from utils.settings import BLUSERS

def is_bot(ctx):
 return ctx.author.bot == False

def is_pop(ctx):
 return ctx.author.id != 393322896568614912
