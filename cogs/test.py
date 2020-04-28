from discordDB import DiscordDB
from discord.ext import commands


LOGS = []
DATABASE_CHANNEL_ID = 704422443808325730


class Database(commands.Cog):

    def __init__(self, bot):
        self.discordDB = DiscordDB(bot, DATABASE_CHANNEL_ID)
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def log(self, ctx, *, text):
        data = {
            "name": ctx.author.name,
            "text": text
        }
        _id = await self.discordDB.set(data)
        LOGS.append(_id)

    @commands.command()
    @commands.is_owner()
    async def show_logs(self, ctx):
        for _id in LOGS:
            data = await self.discordDB.get(_id)
            await ctx.send(f"Name: {data.name}, Text: {data.text}")

def setup(bot):
    bot.add_cog(Database(bot))
