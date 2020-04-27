from discordDB import DiscordDB
from discord.ext import commands


LOGS = []
DATABASE_CHANNEL_ID = 704422443808325730


class MyBot(commands.Bot):

    def __init__(self):
        self.discordDB = DiscordDB(self, DATABASE_CHANNEL_ID)

    @commands.command()
    async def log(self, ctx, *, text):
        data = {
            "name": ctx.author,
            "text": text
        }
        _id = await self.discordDB.set(data)
        LOGS.append(_id)

    @commands.command()
    async def show_logs(self, ctx):
        for _id in LOGS:
            data = await self.discordDB.get(_id)
            await ctx.send(f"Name: {data.name}, Text: {data.text}")


bot = MyBot()
def setup(bot):
    bot.add_cog(MyBot(bot))
