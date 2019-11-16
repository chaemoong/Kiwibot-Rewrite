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
        with open(self.profile) as a:
            json_data = json.load(a)
        utc = datetime.datetime.utcnow()
        dt = datetime.datetime.now()
        dt = '{0.year}-{0.month}-{0.day} {0.hour}:{0.minute}:{0.second}'.format(dt)
        author = ctx.author
        server = author.guild
        self.data[f'{author.id}'] = int(time.perf_counter())
        em = discord.Embed(colour=author.colour, title='잠수 시작! | AFK START!', timestamp=utc)
        em.add_field(name='{} 님의 잠수 상태가 시작되었습니다!'.format(author.name), value='잠수 상태를 해지 하시려면 아무 메시지나 작성해주세요!', inline=False)
        em.set_footer(text=f'Request By: {author}', icon_url=author.avatar_url)
        json_data[f'{author.id}'] = {}
        if reason:
            em.add_field(name='사유', value=reason, inline=False)
            json_data[f'{author.id}'].update({"reason": f"{reason}"})
        else:
            json_data[f'{author.id}'].update({"reason": None})
        with open(self.profile, 'w', encoding="utf-8") as make_file:
            json.dump(json_data, make_file, ensure_ascii=False, indent="\t")
        await ctx.send(author.mention, embed=em)


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
