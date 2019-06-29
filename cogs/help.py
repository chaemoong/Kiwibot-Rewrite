import discord
from discord.ext import commands

class asdf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        await ctx.send('현재 임시로 rewrite 버젼으로 돌아가고 있습니다!\n사용 가능한 명령어: k!userinfo, k!serverinfo')

def setup(bot):
    bot.add_cog(asdf(bot))
