import discord
from discord.ext import commands

class asdf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):

def setup(bot):
    bot.add_cog(asdf(bot))