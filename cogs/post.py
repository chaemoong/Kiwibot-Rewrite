import requests
from bs4 import BeautifulSoup
import json
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO

class post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.company = dataIO.load_json('data/post/company_name.json')

    @commands.command(pass_context=True)
    async def 택배(self, ctx, company_name, tb_number):
        author = ctx.author
        server = ctx.guild
        url = f"https://apis.tracker.delivery/carriers/{company_name}/tracks/{tb_number}"
        req = requests.get(url)
        raw = req.text
        html = BeautifulSoup(raw, 'html.parser')
        a = json.loads(html)
        await ctx.send(str(a['from']))

def setup(bot):
    bot.add_cog(post(bot))
