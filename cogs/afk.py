import discord, datetime, os, time, json
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
        utc = datetime.datetime.utcnow()
        dt = datetime.datetime.now()
        dt = '{0.year}-{0.month}-{0.day} {0.hour}:{0.minute}:{0.second}'.format(dt)
        author = ctx.author
        self.data[f'{author.id}'] = int(time.perf_counter())
        em = discord.Embed(colour=author.colour, title='잠수 시작! | AFK START!', timestamp=utc)
        em.add_field(name='{} 님의 잠수 상태가 시작되었습니다!'.format(author.name), value='잠수 상태를 해지 하시려면 아무 메시지나 작성해주세요!', inline=False)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        self.riceCog[f'{author.id}'] = {}
        if reason:
            em.add_field(name='사유', value=reason, inline=False)
            self.riceCog[f'{author.id}'].update({"reason": f"{reason}"})
        else:
            self.riceCog[f'{author.id}'].update({"reason": None})
        dataIO.save_json(self.profile, self.riceCog)
        await ctx.send(author.mention, embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == True:
            return
        author = message.author
        utc = datetime.datetime.utcnow()
        if f'{message.author.id}' in self.riceCog:
            if 'afk' in message.content:
                return
            else:
                b = self.riceCog[f'{author.id}']['reason']
                if b:
                    a = f'{author.name} 님의 잠수 상태가 끝났습니다!\n\n사유: {b}\n\n어디 다녀 오셨나요!?'
                else:
                    a = f'{author.name} 님의 잠수 상태가 끝났습니다!\n\n어디 다녀 오셨나요!?'
                del self.riceCog[f'{author.id}']
                em = discord.Embed(colour=message.author.colour, timestamp=utc)
                try:
                    em.add_field(name='잠수 끝! | AFK END!', value=a, inline=False)
                except: return
                em.set_footer(text=f'Request By: {author}', icon_url=author.avatar_url)
                return await message.channel.send(embed=em)
        else:
            return


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
