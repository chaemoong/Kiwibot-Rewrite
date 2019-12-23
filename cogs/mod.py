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

    async def owner(ctx):
        ctx.author.id == 431085681847042048

    async def administrator(ctx):
        if ctx.author.id == 431085681847042048:
            return True
        elif ctx.author.guild_permissions.administrator == True:
            return True
    
    @commands.command(pass_context=True, no_pm=True)
    @commands.check(owner)
    async def asdf(self, ctx):
        return await self.send_cmd_help(ctx)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def language(self, ctx, language=None):
        """봇의 언어를 설정하는 명령어 입니다!"""
        server = ctx.guild
        if language == None:
            return await self.language_setting(ctx)
        if language == 'ko':
            try:
                self.data[f'{server.id}'].update({"language": "ko"})
            except KeyError:
                self.data[f'{server.id}'] = {}
                self.data[f'{server.id}'].update({"language": "ko"})
            await ctx.send('> 언어가 성공적으로 `한글` 로 설정 되었습니다! | Succees to language has been set!')
            dataIO.save_json(self.ang, self.data)
        if language == 'en':
            try:
                self.data[f'{server.id}'].update({"language": "en"})
            except KeyError:
                self.data[f'{server.id}'] = {}
                self.data[f'{server.id}'].update({"language": "en"})
            await ctx.send('> 언어가 성공적으로 `영어` 로 설정 되었습니다! | Succees to language has been set!')
            dataIO.save_json(self.ang, self.data)
        else:
            return await self.language_setting(ctx)
            
    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def ban(self, ctx, user:discord.Member=None, *, reason=None):
        """악성 유저를 벤 하는 명령어입니다!"""
        if user == None:
            return await ctx.send('> 벤할 유저를 멘션해주세요!')
        elif reason == None:
            reason = '없음'
        else:
            pass
        try:
            await user.ban(reason=reason)
            await self.logger(ctx, action='벤 | BAN', user=user, reason=reason)   
            return await ctx.send(f'> 벤이 정상적으로 진행되었어요!\n 사유: {reason}')
        except:
            await ctx.send("> 권한이 없거나 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주시고 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!")
            return     

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def unban(self, ctx: commands.Context, user_id: int, *, reason: str = None):
        """유저를 언벤 하는 명령어입니다!"""
        guild = ctx.guild
        if id == None:
            return await ctx.send('> 언벤할 유저의 ID를 적어주세요!')
        elif reason == None:
            reason = '없음'
        else:
            pass
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.errors.NotFound:
            await ctx.send("> 유저를 찾지 못했어요!")
            return
        bans = await guild.bans()
        bans = [be.user for be in bans]
        if user not in bans:
            await ctx.send("> 이 유저는 애초에 벤이 되있지 않습니다! 다시 한번 더 확인해주세요!")
            return
        try:
            await guild.unban(user, reason=reason)
            await self.logger(ctx, action='언벤 | UNBAN', user=user, reason=reason)   
            await ctx.send('> 완료하였습니다!')
        except discord.HTTPException:
            await ctx.send("> 권한이 없거나 혹은 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주시고 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!")
            return     

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(administrator)
    async def hackban(self, ctx: commands.Context, user_id: int, *, reason: str = None):
        """악성유저가 이 서버에 없을경우 대처를 하기 위해 벤하는 명령어입니다!"""
        guild = ctx.guild
        if id == None:
            return await ctx.send('> 핵벤할 유저의 ID를 적어주세요!')
        elif reason == None:
            reason = '없음'
        else:
            pass
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.errors.NotFound:
            await ctx.send("> 유저를 찾지 못했어요!")
            return
        bans = await guild.bans()
        bans = [be.user for be in bans]
        if user in bans:
            await ctx.send("> 이 유저는 애초에 벤이 되있습니다!")
            return
        try:
            await guild.ban(user, reason=reason)
            await ctx.send('> 완료하였습니다!')
            return await self.logger(ctx, action='핵벤 | HACKBAN', user=user, reason=reason)   
        except discord.HTTPException:
            await ctx.send("> 권한이 없거나 혹은 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주시고 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!")

    @commands.command(pass_context=True, no_pm=True, aliases=['warn', 'rudrh', 'ㅈㅁ구'])
    @commands.check(administrator)
    async def 경고(self, ctx, user:discord.Member=None, *, reason=None):
        author = ctx.author
        server = ctx.guild
        if user == None:
            return await ctx.send('> 경고를 줄 유저를 멘션해주세요!')
        if user.bot:
            return await ctx.send('> 봇에게 경고 명령어를 사용할 수 없습니다!')
        if reason == None:
            reason = '없음'
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
            em2.add_field(name=f'당신은 {server.name} 서버에서 벤 당하셨습니다!', value='사유: 경고 초과로 인한 벤')
            em2.set_footer(text=f'만약 반박 하실 내용이 있으시면 {author}({author.id})님에게 문의하세요!')
            await user.send(embed=em2)
            await server.ban(user, reason='경고 누적으로 인한 벤')
            em.add_field(name='경고 발생!', value=f'{user.mention}({user.id})님은 경고 초과로 인하여 벤 되었습니다!')
            self.data2[f'{server.id}'][f'{user.id}'].update({"count": 0})
            self.data2[f'{server.id}'][f'{user.id}']["reason"] = []
            dataIO.save_json(self.warn, self.data2)
        else:          
            em.add_field(name='경고 발생!', value=f'{user.mention} 님은 경고 1회를 받으셨습니다!\n만약 그 유저의 경고가 {all_warn}개가 될경우 그 유저는 벤이 됩니다!\n사유: {reason}\n현재 경고 개수: {count}', inline=False)
            self.data2[f'{server.id}'][f'{user.id}']["reason"].append(f'{count} ' + reason)
            dataIO.save_json(self.warn, self.data2)
        await ctx.send(embed=em)
        return await self.logger(ctx, action='경고 | WARN', user=user, reason=reason)   


    @commands.command(pass_context=True)
    @commands.check(administrator)
    async def unwarn(self, ctx, user:discord.Member=None):
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
        author = ctx.author
        server = ctx.guild
        if user == None:
            user = author
        if user.bot:
            return await ctx.send('> 봇에게 경고 명령어를 사용할 수 없습니다!')
        try:
            count = self.data2[f'{server.id}'][f'{user.id}']["count"]
            if count == 0: return await ctx.send('> 그 유저에 대한 경고데이터가 없습니다!')
        except KeyError:
            return await ctx.send('> 그 유저에 대한 경고데이터가 없습니다!')
        a = self.data2[f'{server.id}'][f'{user.id}']["reason"]
        em = discord.Embed(colour=user.colour)
        em.add_field(name=f'경고 수', value=f'{user.mention} 님의 경고는 {count}개 이며 사유는 아래와 같습니다!')
        for reason in a:
            em.add_field(name=f'사유 {reason[:1]}', value=reason[2:], inline=False)
        await ctx.send(embed=em)

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
        except:
            pass
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
                dataIO.save_json(self.warn, self.data2)
            if admin == None: admin = '없음'
            if mod == None: mod = '없음'
            if log == None: log = '없음'
            await ctx.send(f"```fix\n> 관리자 역할: {admin}\n> 부관리자 역할: {mod}\n> 로그: {log}```\n")
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
        a = dataIO.load_json('data/mod/warning.json')[f'{server.id}'][f'{user.id}']['count']
        b = dataIO.load_json('data/mod/warning.json')[f'{server.id}']['all']
        time = time.strftime("%Y년 %m월 %d일 %H시 %M분 (UTC)".encode('unicode-escape').decode()).encode().decode('unicode-escape')
        em = discord.Embed(colour=author.colour)
        em.add_field(name=action, value=f'발생 시각: {time}', inline=False)
        em.add_field(name='유저(ID) | 관리자(id)', value=f'{author.mention} | {user.mention}', inline=False)
        em.add_field(name='사유', value=reason, inline=False)
        if action == '경고 | WARN' or action == '경고 삭제 | DELETED WARN' or action == '경고 초기화 | RESET WARN':
            em.add_field(name='경고 개수', value=f'{a}/{b}')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await ctx.guild.get_channel(int(log)).send(embed=em)

def setup(bot):
    bot.add_cog(Mod(bot))
