import discord
from discord.ext import commands
import traceback
import json
from discord.utils import get

class Blacklisted(commands.CheckFailure): pass


class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'
   
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        server = ctx.author.guild
        with open(self.setting, encoding='utf-8') as json_file:
            settings = json.load(json_file)
        with open(self.ko, encoding='utf-8') as json_file:
            data1 = json.load(json_file)
        with open(self.en, encoding='utf-8') as json_file:
            data2 = json.load(json_file)
        sangoon = settings["{}".format(server.id)]['languages']
        if sangoon == 'ko':
            lan = data1['command_none']
        elif sangoon == 'en':
            lan = data2['command_none']
        else:
            lan = data2['command_none']
        if isinstance(error, commands.CommandInvokeError):
            # A bit hacky, couldn't find a better way
            no_dms = "Cannot send messages to this user"
            is_help_cmd = ctx.command.qualified_name == "help"
            is_forbidden = isinstance(error.original, discord.Forbidden)
            if is_help_cmd and is_forbidden and error.original.text == no_dms:
                msg = ("당신에게 DM으로 보내드리려고 했는데 전송이 안되요!\nDM차단을 풀어주시면 보내드리겠어요!")
                await ctx.send( msg)
                return

            em = discord.Embed(title='에러발생!', colour=discord.Colour.red())
            em.add_field(name='에러 발생한 명령어', value=ctx.command.qualified_name)
            em.set_footer(text=f'에러가 지속적으로 발생할시 {self.bot.get_user(431085681847042048)}으로 문의 바랍니다!')
            log = ("Exception in command '{}'\n"
                   "".format(ctx.command.qualified_name))
            log += "".join(traceback.format_exception(type(error), error,
                                                      error.__traceback__))
            print(log)
            await ctx.send(embed=em)
        elif isinstance(error, commands.CommandNotFound):
            em = discord.Embed(colour=ctx.author.colour)
            em.add_field(name=lan['1'], value=lan['2'].format(ctx))
            em.set_footer(text=lan['3'])
            await ctx.send(embed=em)
        elif isinstance(error, commands.CheckFailure):
            em = discord.Embed(colour=ctx.author.colour)
            em.add_field(name=lan['1'], value=lan['2'].format(ctx))
            em.set_footer(text=lan['3'])
            await ctx.send(embed=em)

    


def setup(bot):
    bot.add_cog(error(bot))