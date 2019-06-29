import discord
from discord.ext import commands
import traceback

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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
            em.set_footer(text='에러가 지속적으로 발생할시 chaemoong#8612으로 문의 바랍니다!')
            log = ("Exception in command '{}'\n"
                   "".format(ctx.command.qualified_name))
            log += "".join(traceback.format_exception(type(error), error,
                                                      error.__traceback__))
            print(log)
            await ctx.send(embed=em)
        elif isinstance(error, commands.CommandNotFound):
            em = discord.Embed(colour=discord.Colour.red())
            em.add_field(name='없는 명령어 사용 감지!', value='아래의 명령어는 없는 명령어 입니다!')
            em.set_footer(text='제대로 작성하였는지 확인해주시고 사용해주세요!')
            await ctx.send(embed=em)
        elif isinstance(error, commands.CheckFailure):
            em = discord.Embed(colour=discord.Colour.red())
            em.add_field(name='없는 명령어 사용 감지!', value='아래의 명령어는 없는 명령어 입니다!')
            em.set_footer(text='제대로 작성하였는지 확인해주시고 사용해주세요!')
            await ctx.send(embed=em)



def setup(bot):
    bot.add_cog(error(bot))