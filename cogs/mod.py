import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils.dataIO import dataIO
import json
import asyncio
import datetime
from discord.utils import get
original = 10

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ang = 'data/mod/settings.json'
        self.data = dataIO.load_json(self.ang)
        self.warn = 'data/mod/warning.json'
        self.data2 = dataIO.load_json(self.warn)
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'


    async def owner(ctx):
        return ctx.author.id == 431085681847042048

    async def administrator(ctx):
        a = 'data/mod/settings.json'
        b = dataIO.load_json(a)
        if ctx.author.id == 431085681847042048:
            return True
        if ctx.author.guild_permissions.administrator == True:
            return True
        else:
            try:
                admin = get(ctx.author.roles, id=b[f'{ctx.guild.id}']['admin'])
                if admin == None:
                    return False
                else:
                    return True
            except KeyError:
                try:
                    mod = get(ctx.author.roles, id=b[f'{ctx.guild.id}']['mod'])
                    if mod == None:
                        return False
                    else:
                        return True
                except KeyError:
                    return False
                        

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def language(self, ctx, language=None):
        """봇의 언어를 설정하는 명령어 입니다!"""
        server = ctx.guild
        if language == None:
            return await self.language_setting(ctx)
        if language == 'ko_kr' or language == '한글' or language == 'ko':
            try:
                self.data[f'{server.id}'].update({"language": "ko"})
            except KeyError:
                self.data[f'{server.id}'] = {}
                self.data[f'{server.id}'].update({"language": "ko"})
            dataIO.save_json(self.ang, self.data)
            return await ctx.send('> 언어가 성공적으로 `한글` 로 설정 되었습니다! | Success to language has been set!')
        if language == 'en' or language == '영어' or language == 'en':
            try:
                self.data[f'{server.id}'].update({"language": "en"})
            except KeyError:
                self.data[f'{server.id}'] = {}
                self.data[f'{server.id}'].update({"language": "en"})
            dataIO.save_json(self.ang, self.data)
            return await ctx.send('> 언어가 성공적으로 `영어` 로 설정 되었습니다! | Success to language has been set!')
        else:
            return await self.language_setting(ctx)
            
    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def ban(self, ctx, user:discord.Member=None, *, reason=None):
        """악성 유저를 벤 하는 명령어입니다!\nBanned The Person"""
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if user == None:
            return await ctx.send(data['1'])
        elif reason == None:
            reason = data['2']
        else:
            pass
        try:
            await user.ban(reason=reason)
            await self.logger(ctx, action='벤 | BAN', user=user, reason=reason)   
            return await ctx.send(data['3'].format(reason))
        except:
            await ctx.send(data['4'])
            return     

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def unban(self, ctx: commands.Context, user_id: int, *, reason: str = None):
        """유저를 언벤 하는 명령어입니다!\nKicked The Person"""
        guild = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if user_id == None:
            return await ctx.send(data['1'])
        elif reason == None:
            reason = data['2']
        else:
            pass
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.errors.NotFound:
            await ctx.send(data['5'])
            return
        bans = await guild.bans()
        bans = [be.user for be in bans]
        if user not in bans:
            await ctx.send(data['6'])
            return
        try:
            await user.ban(reason=reason)
            await self.logger(ctx, action='언벤 | UNBAN', user=user, reason=reason)   
            return await ctx.send(data['3'].format(reason))
        except:
            await ctx.send(data['4'])
            return     

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def hackban(self, ctx: commands.Context, user_id: int, *, reason: str = None):
        """악성유저가 이 서버에 없을경우 대처를 하기 위해 벤하는 명령어입니다!\nIf the Person is not in this server, ban to protecting"""
        guild = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if user_id == None:
            return await ctx.send(data['1'])
        elif reason == None:
            reason = data['2']
        else:
            pass
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.errors.NotFound:
            await ctx.send(data['3'])
            return
        bans = await guild.bans()
        bans = [be.user for be in bans]
        if user in bans:
            await ctx.send(data['5'])
            return
        try:
            await guild.ban(user, reason=reason)
            await ctx.send(data['3'].format(reason))
            return await self.logger(ctx, action='핵벤 | HACKBAN', user=user, reason=reason)   
        except discord.HTTPException:
            return await ctx.send(data['4'])

    @commands.command(pass_context=True, no_pm=True, aliases=['warn', 'rudrh', 'ㅈㅁ구'])
    @commands.check(administrator)
    async def 경고(self, ctx, user:discord.Member=None, *, reason=None):
        """유저에게 경고를 주는 명령어에요!\nGiving warn to Member"""
        author = ctx.author
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if user == None:
            return await ctx.send(data['7'])
        if user.bot:
            return await ctx.send(data['8'])
        if reason == None:
            reason = data['9']
        try:
            if 'all' in self.data2[f'{server.id}']: pass   
        except KeyError:
            try:
                self.data2[f'{server.id}'].update({"all": original})
            except:
                self.data2[f'{server.id}'] = {}
                self.data2[f'{server.id}'].update({"all": original})
        try:
            if 'count' in self.data2[f'{server.id}'][f'{user.id}']:
                pass
        except KeyError:
            try:
                self.data2[f'{server.id}'][f'{user.id}'].update({"count": 0})
            except:
                self.data2[f'{server.id}'][f'{user.id}'] = {}
                self.data2[f'{server.id}'][f'{user.id}'].update({"count": 0})
        try:
            self.data2[f'{server.id}'][f'{user.id}']["reason"]
        except:
            self.data2[f'{server.id}'][f'{user.id}']["reason"] = []
        dataIO.save_json(self.warn, self.data2)
        count = self.data2[f'{server.id}'][f'{user.id}']["count"]
        all_warn = self.data2[f'{server.id}']["all"]
        count += 1
        self.data2[f'{server.id}'][f'{user.id}'].update({"count": int(count)})
        dataIO.save_json(self.warn, self.data2)
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        if all_warn == count or all_warn < count:
            em2 = discord.Embed(colour=author.colour)
            em2.add_field(name=data['1'].format(server.name), value=data['2'])
            em2.set_footer(text=data['3'].format(author, author.id))
            await user.send(embed=em2)
            await server.ban(user, reason=data['10'])
            em.add_field(name=data['4'], value=data['5'].format(user.mention, user.id))
            self.data2[f'{server.id}'][f'{user.id}'].update({"count": 0})
            self.data2[f'{server.id}'][f'{user.id}']["reason"] = []
            dataIO.save_json(self.warn, self.data2)
        else:          
            em.add_field(name=data['4'], value=data['6'].format(user.mention, all_warn, reason, count), inline=False)
            self.data2[f'{server.id}'][f'{user.id}']["reason"].append(f'{count} ' + reason)
            dataIO.save_json(self.warn, self.data2)
        await ctx.send(embed=em)
        return await self.logger(ctx, action='경고 | WARN', user=user, reason=reason)   


    @commands.command(pass_context=True)
    @commands.check(administrator)
    async def unwarn(self, ctx, user:discord.Member=None):
        """유저에게 경고 1개를 지우는 명령어에요!\nDeleting 1 warn to Member"""
        author = ctx.author
        server = ctx.guild
        if user == None:
            return await ctx.send('> 경고를 지울 유저를 멘션해주세요!')
        if user.bot:
            return await ctx.send('> 봇에게 경고 명령어를 사용할 수 없습니다!')
        try:
            count = self.data2[f'{server.id}'][f'{user.id}']["count"]
        except KeyError:
            return await ctx.send('> 그 유저에 대한 경고데이터가 없습니다!')
        count -= 1
        if count < 0: return await ctx.send('> 그 유저에 대한 경고데이터가 없습니다!')
        self.data2[f'{server.id}'][f'{user.id}'].update({"count": int(count)})
        self.data2[f'{server.id}'][f'{user.id}']["reason"].pop()
        dataIO.save_json(self.warn, self.data2)
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name='성공!', value='그 유저의 경고를 1개 지웠습니다!')
        await ctx.send(embed=em)
        return await self.logger(ctx, action='경고 삭제 | DELETED WARN', user=user, reason=reason)   

    @commands.command(pass_context=True)
    async def check(self, ctx, user:discord.Member=None):
        """유저의 경고를 확인하는 명령어에요!\nDeleting 1 warn to Member"""
        author = ctx.author
        server = ctx.guild
        if user == None:
            user = author
        if user.bot:
            return await ctx.send('> 봇에게 경고 명령어를 사용할 수 없습니다!')
        em = discord.Embed(colour=user.colour)
        try:
            count = self.data2[f'{server.id}'][f'{user.id}']["count"]
            if count == 0: 
                em.add_field(name=f'경고 수', value=f'{user.mention} 님의 경고는 0개입니다!')
                return await ctx.send(embed=em)

        except KeyError:
            em.add_field(name=f'경고 수', value=f'{user.mention} 님의 경고는 0개입니다!')
            return await ctx.send(embed=em)
        a = self.data2[f'{server.id}'][f'{user.id}']["reason"]
        em.add_field(name=f'경고 수', value=f'{user.mention} 님의 경고는 {count}개 이며 사유는 아래와 같습니다!')
        for reason in a:
            em.add_field(name=f'사유 {reason[:1]}', value=reason[2:], inline=False)
        return await ctx.send(embed=em)

    @commands.command(pass_context=True)
    @commands.check(administrator)
    async def clean(self, ctx, user:discord.Member=None, *, reason=None):
        author = ctx.author
        server = ctx.guild
        if user == None:
            user = author
        if user.bot:
            return await ctx.send('> 봇에게 경고 명령어를 사용할 수 없습니다!')
        if reason == None:
            reason = '없음'
        try:
            count = self.data2[f'{server.id}'][f'{user.id}']["count"]
            if count == 0: return await ctx.send('> 그 유저에 대한 경고데이터가 없습니다!')
        except KeyError:
            return await ctx.send('> 그 유저에 대한 경고데이터가 없습니다!')
        a = self.data2[f'{server.id}'][f'{user.id}']["reason"]
        em = discord.Embed(colour=user.colour)
        em.add_field(name=f'성공!', value=f'{user.mention} 님의 경고는 0개로 초기화 되었습니다!')
        for b in range(count):
            a.pop()
        self.data2[f'{server.id}'][f'{user.id}'].update({"count": 0})
        dataIO.save_json(self.warn, self.data2)
        await ctx.send(embed=em)
        return await self.logger(ctx, action='경고 초기화 | RESET WARN', user=user, reason=reason)   


    @commands.group()
    @commands.check(administrator)
    async def warnset(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    
    @warnset.command(pass_context=True)
    async def limit(self, ctx, limit:int=None):
        if limit == None:
            return await ctx.send('> 경고 제한 갯수를 적어주셔야 되요!')
        author = ctx.author
        server = ctx.guild
        try:
            if limit < 1: return await ctx.send('> 경고 제한 갯수는 1 이상 혹은 정수 여야 되요!')
            else: return await ctx.send('> 경고 제한 갯수는 1 이상 혹은 정수 여야 되요!')
        except:
            return await ctx.send('> 경고 제한 갯수는 1 이상 혹은 정수 여야 되요!')        
        try:
            self.data2[f'{server.id}'].update({"all": limit})
        except:
            self.data2[f'{server.id}'] = {}
            self.data2[f'{server.id}'].update({"all": limit})
        dataIO.save_json(self.warn, self.data2)
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name='성공!', value=f'경고 제한을 {limit} 으로 설정했어요!')
        return await ctx.send(embed=em)

    @commands.group()
    @commands.check(administrator)
    async def modset(self, ctx):
        if ctx.invoked_subcommand is None:
            server = ctx.guild
            try:
                if self.data[f'{server.id}']: pass
            except:
                self.data[f'{server.id}'] = {}
            try:
                a = self.data[f'{server.id}']['admin']
                try:
                    if a:
                        admin = get(server.roles, id=a)
                except:
                    admin = '없음'
            except KeyError:
                self.data[f'{server.id}'].update({"admin": '없음'})
                admin = self.data[f'{server.id}']['admin']
            try:
                b = self.data[f'{server.id}']['mod']
                try:
                    if b:
                        mod = get(server.roles, id=b)
                except:
                    mod = '없음'
            except KeyError:
                self.data[f'{server.id}'].update({"mod": '없음'})
                mod = self.data[f'{server.id}']['mod']
            try:
                c = self.data[f'{server.id}']['log']
                try:
                    if c:
                        log = server.get_channel(c)
                except:
                    log = '없음'
            except KeyError:
                self.data[f'{server.id}'].update({"log": '없음'})
                log = self.data[f'{server.id}']['log']
            try:
                d = self.data[f'{server.id}']['dyr']
                try:
                    if d == 'a':
                        d = '켜짐'
                    else: d = '꺼짐'
                except:
                    d = '꺼짐'
            except KeyError:
                self.data[f'{server.id}'].update({"dyr": 'b'})
                d = self.data[f'{server.id}']['dyr']
                dataIO.save_json(self.warn, self.data2)
            if admin == None: admin = '없음'
            if mod == None: mod = '없음'
            if log == None: log = '없음'
            if d == False: d = '꺼짐'
            await ctx.send(f"```fix\n> 관리자 역할: {admin}\n> 부관리자 역할: {mod}\n> 로그: {log}\n> 비속어 필터: {d}```\n")
            return await ctx.send(f'```fix\n> 관리자 역할 설정: {ctx.prefix}{ctx.command} admin [역할]\n> 부관리자 역할 설정: {ctx.prefix}{ctx.command} mod [역할]\n> 로그 설정: {ctx.prefix}{ctx.command} log [채널]```')

    @modset.command(pass_context=True)
    async def admin(self, ctx, role:discord.Role=None):
        if role == None:
            return await ctx.send('역할을 멘션해주셔야 됩니다!')
        author = ctx.author
        server = ctx.guild
        try:
            if self.data[f'{server.id}']: pass
        except:
            self.data[f'{server.id}'] = {}
        try:
            if self.data[f'{server.id}']['admin']:
                del self.data[f'{server.id}']['admin']
                self.data[f'{server.id}'].update({"admin": role.id})
        except KeyError:
            self.data[f'{server.id}'].update({"admin": role.id})
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name='성공!', value=f'{role.name} 역할을 관리자 역할로 정했습니다!')
        await ctx.send(embed=em)
        dataIO.save_json(self.ang, self.data)

    @modset.command(pass_context=True)
    async def mod(self, ctx, role:discord.Role=None):
        if role == None:
            return await ctx.send('역할을 멘션해주셔야 됩니다!')
        author = ctx.author
        server = ctx.guild
        try:
            if self.data[f'{server.id}']['mod']:
                del self.data[f'{server.id}']['mod']
        except:
            self.data[f'{server.id}'] = {}
        self.data[f'{server.id}'].update({"mod": role.id})
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name='성공!', value=f'{role.name} 역할을 부관리자 역할로 정했습니다!')
        await ctx.send(embed=em)
        dataIO.save_json(self.ang, self.data)

    @modset.command(pass_context=True)
    async def log(self, ctx, channel:discord.TextChannel=None):
        if channel == None:
            return await ctx.send('채널을 멘션해주셔야 됩니다!')
        author = ctx.author
        server = ctx.guild
        try:
            if self.data[f'{server.id}']: pass
        except:
            self.data[f'{server.id}'] = {}
        try:
            if self.data[f'{server.id}']['log']:
                del self.data[f'{server.id}']['log']
                self.data[f'{server.id}'].update({"log": channel.id})
        except KeyError:
            self.data[f'{server.id}'].update({"log": channel.id})
        dataIO.save_json(self.ang, self.data)
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name='성공!', value=f'{channel.name} 채널을 로그로 정했습니다!')
        await ctx.send(embed=em)

    @modset.command(pass_context=True)
    async def 욕필터(self, ctx):
        author = ctx.author
        server = ctx.guild
        try:
            if self.data[f'{server.id}']: pass
        except:
            self.data[f'{server.id}'] = {}
        try:
            if self.data[f'{server.id}']['dyr'] == 'a':
                del self.data[f'{server.id}']['dyr']
                self.data[f'{server.id}'].update({"dyr": 'b'})
            else:
                del self.data[f'{server.id}']['dyr']
                self.data[f'{server.id}'].update({"dyr": 'a'})
        except KeyError:
            self.data[f'{server.id}'].update({"dyr": 'a'})        
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        if self.data[f'{server.id}']['dyr'] == 'a':
            b = '켜'
        else:
            b = '꺼'
        dataIO.save_json(self.ang, self.data)
        em.add_field(name='성공!', value=f'욕필터를 {b}졌습니다!')
        await ctx.send(embed=em)



    async def send_cmd_help(self, ctx):
        c = self.bot.get_channel(ctx.message.channel.id)
        em = discord.Embed(colour=ctx.author.colour)
        em.add_field(name='그 명령어는 없는 명령어입니다!', value='`{0.prefix}help` 으로 확인하세요!'.format(ctx))
        em.set_footer(text='제대로 작성하였는지 확인해주시고 사용해주세요!')
        return await c.send(embed=em)

    async def language_setting(self, ctx):
        author = ctx.author
        c = self.bot.get_channel(ctx.message.channel.id)
        em = discord.Embed(colour=author.colour, title=':thinking: 언어 설정 | LANGUAGE SETTINGS :thinking:', timestamp=datetime.datetime.utcnow())
        em.add_field(name='사용 가능한 언어 | AVAILABLE LANGUAGES', value=':arrow_right: ko_kr(한글), en_us(영어) :arrow_left:')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await c.send(embed=em)

    async def logger(self, ctx, action, user, reason=None):
        server = ctx.guild
        author = ctx.author
        try:
            log = dataIO.load_json('data/mod/settings.json')[f'{server.id}']['log']
        except KeyError: 
            return
        time = datetime.datetime.now()
        if reason == None:
            reason = '없음'
        time = time.strftime("%Y년 %m월 %d일 %H시 %M분 (UTC)".encode('unicode-escape').decode()).encode().decode('unicode-escape')
        em = discord.Embed(colour=author.colour)
        em.add_field(name=action, value=f'발생 시각: {time}', inline=False)
        em.add_field(name='유저(ID) | 관리자(id)', value=f'{author.mention} | {user.mention}', inline=False)
        em.add_field(name='사유', value=reason, inline=False)
        if action == '경고 | WARN' or action == '경고 삭제 | DELETED WARN' or action == '경고 초기화 | RESET WARN':
            a = dataIO.load_json('data/mod/warning.json')[f'{server.id}'][f'{user.id}']['count']
            b = dataIO.load_json('data/mod/warning.json')[f'{server.id}']['all']
            em.add_field(name='경고 개수', value=f'{a}/{b}')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await ctx.guild.get_channel(int(log)).send(embed=em)

def setup(bot):
    bot.add_cog(Mod(bot))
