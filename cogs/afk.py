import discord, datetime, os, time, json, settings
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from pymongo import MongoClient
set = settings.set()
try:
    client = MongoClient(host=set.ip, port=set.port, username=set.user, password=set.pwd, authSource=set.auth)    
    db = client['chaemoong']['afk']
    lang = client['chaemoong']['mod.language'].find_one
except:
    print("AFK Cog에서 몽고DB를 연결할 수 없습니다!")

class Afk(commands.Cog):
    """asdf!"""

    def __init__(self, bot):
        self.bot = bot
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'


    @commands.command(no_pm=True, name='afk', description='The afk command! | 잠수 명령어입니다!', aliases=['ㅁ라', '잠수', 'wkatn'])
    async def afk(self, ctx, *, reason=None):
        """잠수 명령어 입니다!"""
        utc = datetime.datetime.utcnow()
        dt = datetime.datetime.now()
        dt = '{0.year}-{0.month}-{0.day} {0.hour}:{0.minute}:{0.second}'.format(dt)
        author = ctx.author
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        try:
            dbdata = {"_id": author.id, "reason": f"{reason}"}
            if reason:
                em.add_field(name=data['4'], value=reason, inline=False)
            try:
                db.insert_one(dbdata)
            except:
                db.delete_one({"_id": author.id})
                db.insert_one(dbdata)
            await ctx.send(author.mention, embed=em)
        except: return await ctx.send('봇에 장애가 발생하였습니다. 잠시후 사용해주세요')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == True:
            return
        author = message.author
        utc = datetime.datetime.utcnow()
        try:
            try:
                asdf = lang({'_id': message.guild.id})
                if asdf['language'] == 'ko':
                    data = dataIO.load_json(self.ko)["end"]
                else:
                    data = dataIO.load_json(self.en)["end"]
            except:
                data = dataIO.load_json(self.en)["end"]
            if db.find_one({"_id": author.id}):
                aliases= ['afk', 'ㅁ라', '잠수', 'wkatn']
                for a in aliases:
                    if a in message.content:
                        return
                else:
                    try:
                        b = db.find_one({"_id": author.id})
                    except:
                        return
                    if str(b['reason']) == str(None):
                        a = data['2'].format(author.name)
                    else:
                        a = data['1'].format(author.name, b['reason'])
                    db.delete_one({"_id": author.id})
                    em = discord.Embed(colour=message.author.colour, timestamp=utc)
                    try:
                        em.add_field(name=data['3'], value=a, inline=False)
                    except: return
                    em.set_footer(text=f'Request By: {author}', icon_url=author.avatar_url)
                    await message.channel.send(embed=em)
                    return
            else:
                return
        except: return

def setup(bot):
    bot.add_cog(Afk(bot))
