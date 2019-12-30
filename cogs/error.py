import discord
from discord.ext import commands
import traceback
import json
from discord.utils import get
from cogs.utils.dataIO import dataIO

class Blacklisted(commands.CheckFailure): pass


class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'
        self.asdf = dataIO.load_json('data/mod/list.json')
   
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        yee = dataIO.load_json(self.setting)
        try:
            if yee[f'{ctx.guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)
            else:
                data = dataIO.load_json(self.en)
        except:
            data = dataIO.load_json(self.en)
        if isinstance(error, commands.CommandInvokeError):
            # A bit hacky, couldn't find a better way
            no_dms = "Cannot send messages to this user"
            is_help_cmd = ctx.command.qualified_name == "help"
            is_forbidden = isinstance(error.original, discord.Forbidden)
            if is_help_cmd and is_forbidden and error.original.text == no_dms:
                msg = ("당신에게 DM으로 보내드리려고 했는데 전송이 안되요! DM차단을 풀어주시면 다시 시도 하시면 보내드리겠어요!\nI was going to send it to you by DM, but it's not! If you untie the DM block, I'll send it to you!")
                await ctx.send(msg)
                return
            em = discord.Embed(title='에러! | ERROR!', colour=discord.Colour.red())
            em.add_field(name='에러 발생한 명령어 | Error generated command', value=ctx.command.qualified_name)
            em.set_footer(text=f'에러가 지속적으로 발생할시 {self.bot.get_user(431085681847042048)}으로 문의 바랍니다!\nIf that command Error generated again contact {self.bot.get_user(431085681847042048)} ({self.bot.get_user(431085681847042048).id})')
            log = ("Exception in command '{}'\n"
                   "".format(ctx.command.qualified_name))
            log += "".join(traceback.format_exception(type(error), error,
                                                      error.__traceback__))
            print(log)
            await ctx.send(embed=em)
        elif isinstance(error, commands.CommandNotFound):
            lan = data['command_none']
            em = discord.Embed(colour=ctx.author.colour)
            em.add_field(name=lan['1'], value=lan['2'].format(ctx))
            em.set_footer(text=lan['3'])
            return await ctx.send(embed=em)
        elif isinstance(error, commands.CheckFailure):
            lan = data['admin_command']
            em = discord.Embed(colour=ctx.author.colour)
            em.add_field(name=lan['1'], value=lan['2'].format(ctx))
            em.set_footer(text=lan['3'])
            return await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == True:
            return
        
          
    


def setup(bot):
    bot.add_cog(error(bot))
