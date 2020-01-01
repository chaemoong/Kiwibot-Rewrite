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
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'


    @commands.command(no_pm=True, name='afk', description='The afk command! | 잠수 명령어입니다!', aliases=['ㅁ라', '잠수', 'wkatn'])
    async def afk(self, ctx, *, reason=None):
        """잠수 명령어 입니다!"""
        utc = datetime.datetime.utcnow()
        dt = datetime.datetime.now()
        dt = '{0.year}-{0.month}-{0.day} {0.hour}:{0.minute}:{0.second}'.format(dt)
        author = ctx.author
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{ctx.guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        em = discord.Embed(colour=author.colour, title=data['1'], timestamp=utc)
        em.add_field(name=data['2'].format(author.name), value=data['3'], inline=False)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        self.riceCog[f'{author.id}'] = {}
        if reason:
            em.add_field(name=data['4'], value=reason, inline=False)
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
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{message.guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)["end"]
            else:
                data = dataIO.load_json(self.en)["end"]
        except:
            data = dataIO.load_json(self.en)["end"]
        if f'{message.author.id}' in self.riceCog:
            if 'afk' in message.content:
                return
            else:
                try:
                    b = self.riceCog[f'{author.id}']['reason']
                except:
                    return
                if b:
                    a = data['1'].format(author.name, b)
                else:
                    a = data['2'].format(author.name)
                self.riceCog[f'{author.id}'] = {}
                del self.riceCog[f'{author.id}']
                em = discord.Embed(colour=message.author.colour, timestamp=utc)
                try:
                    em.add_field(name=data['3'], value=a, inline=False)
                except: return
                em.set_footer(text=f'Request By: {author}', icon_url=author.avatar_url)
                await message.channel.send(embed=em)
                dataIO.save_json(self.profile, self.riceCog)
                return
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
