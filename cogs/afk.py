import discord, datetime, os, time
from discord.ext import commands
from cogs.utils.dataIO import dataIO


class Afk(commands.Cog):
    """asdf!"""

    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.profile = "data/afk/afk.json"
        self.riceCog = dataIO.load_json(self.profile)
        
    @commands.command(no_pm=True, pass_context=True)
    async def afk(self, ctx, *, reason=None):
        """잠수 명령어 입니다!"""
        dt = datetime.datetime.now()
        dt = '{}-{}-{} {}:{}:{}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        author = ctx.author
        server = author.guild
        em = discord.Embed(colour=author.colour, title='잠수 시작! | AFK START!')
        em.add_field(name='{} 님의 잠수 상태가 시작되었습니다!'.format(author.name), value='잠수 상태를 해지 하시려면 아무 메시지나 작성해주세요!', inline=False)
        if reason:
            em.add_field(name='사유', value=reason, inline=False)
        else:
            pass
        await ctx.send(embed=em)
        self.riceCog[author.id] = {}
        self.riceCog[author.id].update({"reason": str(reason)})
        dataIO._save_json(self.profile,
                     self.riceCog)        
        await ctx.send(embed=em)
                
def check_folder():
    if not os.path.exists('data/afk'):
        print('data/afk 풀더생성을 완료하였습니다!')
        os.makedirs('data/afk')

def check_file():
    data = {}
    f = "data/afk/afk.json"
    if not dataIO.is_valid_json(f):
        print("afk.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Afk(bot))
