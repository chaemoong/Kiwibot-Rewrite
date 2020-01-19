"""coding: UTF-8, coding by: discordtag: chaemoong#9454"""
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils.dataIO import dataIO
import json
import asyncio
import datetime
from discord.utils import get
import os

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
        self.asdfasdf = 'prefix.json'
        self.prefix = dataIO.load_json(self.asdfasdf)
        self.level = 'data/mod/settings.json'
        self.leveling = dataIO.load_json(self.level)
        self.welcome = 'data/mod/welcome.json'

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

    @commands.command(no_pm=True, name='autorole', description='The autorole setting command! | 자동으로 역할이 들어오게 설정하는 명령어입니다!', aliases=['며새개ㅣㄷ', '자동역할', 'wkehddurgkf'])
    @commands.check(administrator)
    async def autorole(self, ctx, role:discord.Role=None, emoji=None, *, message=None):
        author = ctx.author
        server = ctx.guild
        if role == None:
            return await ctx.send('> 역할을 멘션 해주시거나 역할의 ID를 적어주셔야죠!')
        if emoji == None:
            return await ctx.send('> 이모지를 적어주셔야죠!')
        if message == None:
            return await ctx.send('> 메시지를 적어주셔야죠!')
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        if message.startswith == '@everyone':
            a = message[9:]
            em.add_field(name='메시지', value=a)
            asdf = await ctx.send('@everyone', embed=em)
        else:
            a = message
            em.add_field(name='메시지', value=a)
            asdf = await ctx.send(embed=em)
        await asdf.add_reaction(emoji)
        def check(reaction, user):
            if user.bot == True:
                return False
            if server.id == user.guild.id and str(reaction.emoji) == emoji: 
                return True
        thinking = await self.bot.wait_for('reaction_add', check=check)
        while True:
            if True:
                fffffff = thinking[1].id
                try:
                    await server.get_member(fffffff).add_roles(role)
                    thinking = await self.bot.wait_for('reaction_add', check=check)
                except:
                    await ctx.send('> 역할이 삭제 되었거나 권한이 부족합니다! 메시지를 삭제하겠습니다!')
                    await asdf.delete()
                    break

    @commands.command(no_pm=True, name='language', description='The language setting command! | 언어를 선택하는 명령어입니다!', aliases=['ㅣ무혐ㅎㄷ', '언어', 'djsdj'])
    @commands.check(administrator)
    async def language(self, ctx):
        """봇의 언어를 설정하는 명령어 입니다!"""
        server = ctx.guild
        author = ctx.author
        em = discord.Embed(colour=author.colour, title='언어 설정 | LANGUAGE SETTINGS', timestamp=datetime.datetime.utcnow())
        em.add_field(name='사용 가능한 언어 | AVAILABLE LANGUAGES', value=':arrow_right: 한국어 :flag_kr:, English :flag_us: :arrow_left:')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        a = await ctx.send(embed=em)
        await a.add_reaction('🇰🇷')
        await a.add_reaction('🇺🇸')
        asdf = ['🇰🇷', '🇺🇸']
        def check(reaction, user):
            if user == ctx.author and str(reaction.emoji) in asdf: 
                return True 
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await a.edit(content='> 정상적으로 취소되었습니다!')
        if True:
            await a.delete()
            if str(reaction.emoji) == '🇰🇷':
                try:
                    self.data[f'{server.id}'].update({"language": "ko"})
                except KeyError:
                    self.data[f'{server.id}'] = {}
                    self.data[f'{server.id}'].update({"language": "ko"})
                dataIO.save_json(self.ang, self.data)
                return await ctx.send('> 언어가 성공적으로 `한글` 로 설정 되었습니다!')            
            if str(reaction.emoji) == '🇺🇸':
                try:
                    self.data[f'{server.id}'].update({"language": "en"})
                except KeyError:
                    self.data[f'{server.id}'] = {}
                    self.data[f'{server.id}'].update({"language": "en"})
                dataIO.save_json(self.ang, self.data)
                return await ctx.send('> Language has been successfully set as `English`')        
        else:
            return await ctx.send("> 다른 이모지를 추가하지 마세요! | Please don't add another emoji")

    @commands.command(no_pm=True, name='ban', description='It is a user-banning command. | 유저를 벤하는 명령어입니다!', aliases=['ㅠ무', '벤', 'qps', '차단', 'ckeks'])
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

    @commands.command(no_pm=True, name='unban', description='It is a user-unbanning command. | 유저를 언벤하는 명령어입니다!', aliases=['ㅕㅜㅠ무', '언벤', 'djsqps', '차단해제', 'ckeksgowp'])
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
            await user.unban(reason=reason)
            await self.logger(ctx, action='언벤 | UNBAN', user=user, reason=reason)   
            return await ctx.send('> 완료했습니다!')
        except:
            await ctx.send(data['4'])
            return     

    @commands.command(no_pm=True, name='hackban', description='It is a user-hackbanning command. | 유저를 핵벤하는 명령어입니다!', aliases=['ㅗㅁ차ㅠ무', '핵벤', 'gorqps', '강제차단', 'rkdwpckeks'])
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

    @commands.command(no_pm=True, name='warn', description='It is a user-warnning command. | 유저를 경고하는 명령어입니다!', aliases=['ㅈㅁ구', 'rudrh'])
    @commands.check(administrator)
    async def 경고(self, ctx, user:discord.Member=None, *, reason=None):
        """유저에게 경고를 주는 명령어에요!\nGiving warn to Member"""
        author = ctx.author
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['경고']
            else:
                data = dataIO.load_json(self.en)['경고']
        except:
            data = dataIO.load_json(self.en)['경고']
        if user == None:
            return await ctx.send(data['7'])
        if user == author:
            return await ctx.send(data['me'])
        if user.bot:
            return await ctx.send(data['8'])
        if reason == None:
            reason = data['9']
        try:
            if not 'all' in self.data2[f'{server.id}']: self.data2[f'{server.id}'].update({"all": original})   
        except KeyError:
            try:
                self.data2[f'{server.id}'].update({"all": original})
            except:
                self.data2[f'{server.id}'] = {}
                self.data2[f'{server.id}'].update({"all": original})
        try:
            if not 'count' in self.data2[f'{server.id}'][f'{user.id}']:
                self.data2[f'{server.id}'][f'{user.id}'] = {}
                self.data2[f'{server.id}'][f'{user.id}'].update({"count": 0})
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
        em = discord.Embed(colour=author.colour, title=server.name, timestamp=datetime.datetime.utcnow())
        dkdk = self.data2[f'{server.id}']["all"]
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        if all_warn == count or all_warn < count:
            asdf = self.data2[f'{server.id}'][f'{user.id}'].get('count')
            em2 = discord.Embed(colour=author.colour, title=server.name, timestamp=datetime.datetime.utcnow())
            em2.add_field(name='Administrator', value=author)
            em2.add_field(name='USER', value=user, inline=False)
            em2.add_field(name='사유', value='경고 초과로 인한 벤', inline=False)
            em2.add_field(name='경고 갯수', value=f'{asdf} / {dkdk}', inline=False)
            if author.avatar_url:
                em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
            else:
                em.set_footer(text=f'Request By {author}')
            try:
                await server.ban(user, reason=data['10'])
                await user.send(embed=em2)
            except:
                self.data2[f'{server.id}'][f'{user.id}']["reason"].append(f'{count} ' + reason)
                dataIO.save_json(self.warn, self.data2)
                return await ctx.send('권한이 없거나 그 유저가 봇보다 권한이 높습니다!\n봇에 권한을 추가 해주시거나 권한을 높여주세요!')
            em.add_field(name=data['4'], value=data['5'].format(user.mention, user.id))
            self.data2[f'{server.id}'][f'{user.id}'].update({"count": 0})
            self.data2[f'{server.id}'][f'{user.id}']["reason"] = []
            dataIO.save_json(self.warn, self.data2)
        else:
            really = self.data2[f'{server.id}'][f'{user.id}'].get('count')
            em.add_field(name='Administrator', value=author)
            em.add_field(name='USER', value=user, inline=False)
            em.add_field(name='사유', value=reason, inline=False)
            em.add_field(name='경고 갯수 / 경고 제한', value=f'{really} / {dkdk}', inline=False)
            em.set_thumbnail(url=server.icon_url)
            self.data2[f'{server.id}'][f'{user.id}']["reason"].append(f'{count} ' + reason)
            dataIO.save_json(self.warn, self.data2)
        await ctx.send(embed=em)
        return await self.logger(ctx, action='경고 | WARN', user=user, reason=reason)   


    @commands.command(no_pm=True, name='unwarn', description='It is a user-unwarnning command. | 유저를 경고한개를 삭제하는 명령어입니다!', aliases=['ㅕㅜㅈㅁ구', '경고지우기', 'rudrhwldnrl'])
    @commands.check(administrator)
    async def unwarn(self, ctx, user:discord.Member=None, reason=None):
        """유저에게 경고 1개를 지우는 명령어에요!\nDeleting 1 warn to Member"""
        author = ctx.author
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
        if user.bot:
            return await ctx.send(data['2'])
        if reason==None:
            reason = data['3']
        try:
            count = self.data2[f'{server.id}'][f'{user.id}']["count"]
        except KeyError:
            return await ctx.send(data['4'])
        count -= 1
        if count < 0: return await ctx.send(data['4'])
        self.data2[f'{server.id}'][f'{user.id}'].update({"count": int(count)})
        self.data2[f'{server.id}'][f'{user.id}']["reason"].pop()
        dataIO.save_json(self.warn, self.data2)
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name=data['5'], value=data['6'])
        await ctx.send(embed=em)
        return await self.logger(ctx, action='경고 삭제 | DELETED WARN', user=user, reason=reason)   

    @commands.command(no_pm=True, name='check', description='It is a user-warnning check command. | 유저의 경고를 확인하는 명령어입니다!', aliases=['경고확인', '촏차', 'rudrhghkrdls'])
    async def check(self, ctx, user:discord.Member=None):
        """유저의 경고를 확인하는 명령어에요!\nDeleting 1 warn to Member"""
        author = ctx.author
        server = ctx.guild
        if user == None:
            user = author
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if user.bot:
            return await ctx.send(data['2'])
        em = discord.Embed(colour=user.colour)
        try:
            count = self.data2[f'{server.id}'][f'{user.id}']["count"]
            if count == 0: 
                em.add_field(name=data['3'], value=data['5'].format(user.mention))
                return await ctx.send(embed=em)

        except KeyError:
            em.add_field(name=data['3'], value=data['5'].format(user.mention))
            return await ctx.send(embed=em)
        a = self.data2[f'{server.id}'][f'{user.id}']["reason"]
        em.add_field(name=data['3'], value=data['6'].format(user.mention, count))
        for reason in a:
            em.add_field(name=data['7'].format(reason[:2]), value=reason[2:], inline=False)
        return await ctx.send(embed=em)

    @commands.command(no_pm=True, name='clean', description='It is a user-warnning cleaning command. | 유저의 경고를 삭제하는 명령어입니다!', aliases=['칟무', '경고삭제', 'rudrhtkrwp'])
    @commands.check(administrator)
    async def clean(self, ctx, user:discord.Member=None, *, reason=None):
        author = ctx.author
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
        if user.bot:
            return await ctx.send(data['2'])
        if reason == None:
            reason = data['3']
        try:
            count = self.data2[f'{server.id}'][f'{user.id}']["count"]
            if count == 0: return await ctx.send(data['4'])
        except KeyError:
            return await ctx.send(data['4'])
        em = discord.Embed(colour=user.colour)
        em.add_field(name=data['5'], value=data['6'].format(user.mention))
        self.data2[f'{server.id}'][f'{user.id}'] = {}
        dataIO.save_json(self.warn, self.data2)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        await ctx.send(embed=em)
        return await self.logger(ctx, action='경고 초기화 | RESET WARN', user=user, reason=reason)   

    @commands.command(no_pm=True, name='limit', description='limit command that limits the number of warnings on the server. | 서버의 경고수를 제한하는 명령어입니다!', aliases=['ㅣㅑㅡㅑㅅ', '경고제한', 'rudrhwpgks'])
    async def limit(self, ctx, limit:int=None):
        """경고제한 하는 명령어입니다! | This command limits the warning!"""
        author = ctx.author
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if limit == None:
            return await ctx.send(data['2'])
        author = ctx.author
        server = ctx.guild
        try:
            if limit < 1: return await ctx.send(data['1'])
        except:
            return await ctx.send(data['1'])        
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
        em.add_field(name=data['5'], value=data['6'].format(limit))
        return await ctx.send(embed=em)
    
    @commands.command(no_pm=True)
    @commands.check(administrator)
    async def setprefix(self, ctx, *, prefixes=None):
        if prefixes == None:
            return await ctx.send('접두사를 적어주세요! | Write Down Prefix')
        self.prefix[str(ctx.guild.id)] = {}
        self.prefix[str(ctx.guild.id)].update({"prefix": prefixes or 'c!'})
        await ctx.send("Prefixes set!")
        dataIO.save_json(self.asdfasdf, self.prefix)

    @commands.group(no_pm=True, name='lvlset', description='Commands to set leveling functions! | 레벨링 기능들을 설정하는 명령어입니다!', aliases=['ㅣ핀ㄷㅅ', '레벨설정', 'fpqpftjfwjd'])
    @commands.check(administrator)
    async def lvlset(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(colour=discord.Colour.orange(), title='레벨링 설정 | Leveling Funcion Settings', timestamp=datetime.datetime.utcnow())
            em.add_field(name='아래에는 사용 가능한 명령어들입니다!', value='onoff - 레벨링 기능을 껐다 킬수 있도록 설정합니다!')
            return await ctx.send(ctx.author.mention, embed=em)

    @lvlset.command(pass_context=True)
    async def onoff(self, ctx):
        server = ctx.guild
        author = ctx.author
        em = discord.Embed(colour=author.colour, title='온오프 설정 | ON OR OFF SETTINGS', timestamp=datetime.datetime.utcnow())
        em.add_field(name='레벨업 메시지 보내기 기능을 켜실건가요? 끄실건가요? | Are you turn on sending leveling? or turn off sending leveling message?', value='켜실려면 ⭕ 끄실거면 ❌에 반응해주세요!')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        a = await ctx.send(embed=em)
        await a.add_reaction('⭕')
        await a.add_reaction('❌')
        asdf = ['⭕', '❌']
        def check(reaction, user):
            if user == ctx.author and str(reaction.emoji) in asdf: 
                return True 
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await a.edit(content='> 정상적으로 취소되었습니다!')
        if True:
            em2 = discord.Embed(colour=author.colour, title='온오프 설정 | ON OR OFF SETTINGS', timestamp=datetime.datetime.utcnow())
            if reaction.emoji == '⭕':
                if self.data.get(f'{server.id}') == None:
                    self.data[str(server.id)] = {}
                self.data[str(server.id)].update({"level": "on"})
                dataIO.save_json(self.level, self.data)
                em2.add_field(name='성공!', value='이 서버에서 발생하는 레벨링 메시지를 켰습니다!')
                return await a.edit(content=author.mention, embed=em2)
            if reaction.emoji == '❌':
                if self.data.get(f'{server.id}') == None:
                    self.data[str(server.id)] = {}
                self.data[str(server.id)].update({"level": "off"})
                dataIO.save_json(self.level, self.data)
                em2.add_field(name='성공!', value='이 서버의 레벨링 메시지를 껐습니다!')
                return await a.edit(content=author.mention, embed=em2)
            else:
                return await a.edit(content='이상한 이모지를 추가하지 마세요!')

                

    @commands.group(no_pm=True, name='modset', description='Commands to set administrator functions! | 관리자 기능들을 설정하는 명령어입니다!', aliases=['ㅡㅐㅇㄴㄷㅅ', '관리자기능설정', 'rhksflwkrlsmdtjfwjd'])
    @commands.check(administrator)
    async def modset(self, ctx):
        author =  ctx.author
        if ctx.invoked_subcommand is None:
            server = ctx.guild
            asdf = dataIO.load_json(self.setting)
            try:
                if asdf[f'{server.id}']['language'] == 'ko':
                    data = dataIO.load_json(self.ko)['modset']
                else:
                    data = dataIO.load_json(self.en)['modset']
            except:
                data = dataIO.load_json(self.en)['modset']
            try:
                if self.data[f'{server.id}']: pass
                try:
                    a = self.data[f'{server.id}'].get('admin')
                    try:
                        if a == None:
                            admin = data['None']
                        if a:
                            admin = get(server.roles, id=a)
                            if admin == None:
                                admin = data['realnone']
                    except:
                        admin = data['None']
                except KeyError:
                    admin = data['None']
                try:
                    b = self.data[f'{server.id}'].get('mod')
                    try:
                        if b == None:
                            mod = data['None']
                        if b:
                            mod = get(server.roles, id=b)
                            if mod == None:
                                mod = data['realnone']
                    except:
                        mod = data['realnone']
                except KeyError:
                    mod = data['None']
                try:
                    c = self.data[f'{server.id}'].get('log')
                    try:
                        if c == None: log = data['None']
                        if c:
                            log = server.get_channel(c)
                    except:
                        log = data['realnone']
                except KeyError:
                    log = data['None']
                try:
                    e = self.data[f'{server.id}'].get('rold')
                    try:
                        if e:
                            rold = get(server.roles, id=e)
                            if rold == None:
                                rold = data['realnone']
                        if e == None:
                            rold = data['None']
                    except:
                        rold = data['realnone']
                except KeyError:
                    rold = data['None']
            except:
                self.data[f'{server.id}'] = {}
                admin = data['None']
                mod = data['None']
                log = data['None']
                rold = data['None']
            try:
                asdfasdf = self.bot.get_cog('Music').setting.get(str(server.id)).get('volume')
            except:
                asdfasdf = None
            if not log: log = data['None']
            if asdfasdf == None:
                volume = '100'
            else:
                volume = asdfasdf
            em = discord.Embed(colour=ctx.author.colour)        
            em.add_field(name=':passport_control:' + data['first'], value=data['embed1'].format(admin, mod, rold))
            em.add_field(name=':newspaper:' + data['second'], value=data['embed2'].format(log))
            em.add_field(name=':musical_note:' + data['third'], value=data['embed3'].format(volume))
            em.add_field(name=data['basic']['a'], value=data['basic']['admin'].format(ctx))
            if author.avatar_url:
                em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
            else:
                em.set_footer(text=f'Request By {author}')
            return await ctx.send(author.mention, embed=em)

    @modset.command(pass_context=True)
    async def admin(self, ctx, role:discord.Role=None):
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['modset']['admin']
            else:
                data = dataIO.load_json(self.en)['modset']['admin']
        except:
            data = dataIO.load_json(self.en)['modset']['admin']
        if role == None:
            return await ctx.send(data['1'])
        author = ctx.author
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
        em.add_field(name=data['2'], value=data['3'].format(role.name))
        await ctx.send(embed=em)
        dataIO.save_json(self.ang, self.data)

    @modset.command(pass_context=True)
    async def mod(self, ctx, role:discord.Role=None):
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['modset']['mod']
            else:
                data = dataIO.load_json(self.en)['modset']['mod']
        except:
            data = dataIO.load_json(self.en)['modset']['mod']
        if role == None:
            return await ctx.send(data['1'])
        author = ctx.author
        try:
            if self.data[f'{server.id}']: pass
        except:
            self.data[f'{server.id}'] = {}
        try:
            if self.data[f'{server.id}']['mod']:
                del self.data[f'{server.id}']['mod']
                self.data[f'{server.id}'].update({"mod": role.id})
        except KeyError:
            self.data[f'{server.id}'].update({"mod": role.id})
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name=data['2'], value=data['3'].format(role.name))
        await ctx.send(embed=em)
        dataIO.save_json(self.ang, self.data)

    @modset.command(pass_context=True)
    async def log(self, ctx, channel:discord.TextChannel=None):
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['modset']['log']
            else:
                data = dataIO.load_json(self.en)['modset']['log']
        except:
            data = dataIO.load_json(self.en)['modset']['log']
        if channel == None:
            return await ctx.send(data['1'])
        author = ctx.author
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
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name=data['2'], value=data['3'].format(channel.name))
        await ctx.send(embed=em)
        dataIO.save_json(self.ang, self.data)

    @modset.command(pass_context=True)
    async def 욕필터(self, ctx):
        author = ctx.author
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['modset']['filter']
            else:
                data = dataIO.load_json(self.en)['modset']['filter']
        except:
            data = dataIO.load_json(self.en)['modset']['filter']
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
            b = data['1']
        else:
            b = data['2']
        dataIO.save_json(self.ang, self.data)
        em.add_field(name=data['3'], value=data['4'].format(b))
        await ctx.send(embed=em)

    @modset.command(pass_context=True)
    async def role(self, ctx, role:discord.Role=None):
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['modset']['role']
            else:
                data = dataIO.load_json(self.en)['modset']['role']
        except:
            data = dataIO.load_json(self.en)['modset']['role']
        if role == None:
            return await ctx.send(data['1'])
        author = ctx.author
        try:
            if self.data[f'{server.id}']: pass
        except:
            self.data[f'{server.id}'] = {}
        try:
            if self.data[f'{server.id}']['rold']:
                del self.data[f'{server.id}']['rold']
                self.data[f'{server.id}'].update({"rold": role.id})
        except KeyError:
            self.data[f'{server.id}'].update({"rold": role.id})
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name=data['2'], value=data['3'].format(role.name))
        await ctx.send(embed=em)
        dataIO.save_json(self.ang, self.data)

    @modset.command(pass_context=True)
    async def channel(self, ctx, channel:discord.TextChannel=None):
        server = ctx.guild
        asdf = dataIO.load_json(self.setting)
        await ctx.send(channel.id)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['modset']['channel']
            else:
                data = dataIO.load_json(self.en)['modset']['channel']
        except:
            data = dataIO.load_json(self.en)['modset']['channel']
        if channel == None:
            return await ctx.send(data['1'])
        author = ctx.author
        try:
            if self.data[f'{server.id}']: pass
        except:
            self.data[f'{server.id}'] = {}
        self.data[f'{server.id}'].update({"channel": channel.id})
        em = discord.Embed(colour=author.colour)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.add_field(name=data['2'], value=data['3'].format(channel.name))
        await ctx.send(embed=em)
        dataIO.save_json(self.ang, self.data)

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
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)['log']
            else:
                data = dataIO.load_json(self.en)['log']
        except:
            data = dataIO.load_json(self.en)['log']
        try:
            log = dataIO.load_json('data/mod/settings.json')[f'{server.id}']['log']
        except KeyError: 
            return
        time = datetime.datetime.now()
        if reason == None:
            reason = data['1']
        time = time.strftime(data['2'].encode('unicode-escape').decode()).encode().decode('unicode-escape')
        em = discord.Embed(colour=author.colour)
        em.add_field(name=action, value=data['3'].format(time), inline=False)
        em.add_field(name=data['4'], value=f'{author.mention} ({author.id}) | {user.mention} ({user.id})', inline=False)
        em.add_field(name=data['5'], value=reason, inline=False)
        if action == '경고 | WARN' or action == '경고 삭제 | DELETED WARN' or action == '경고 초기화 | RESET WARN':
            a = dataIO.load_json('data/mod/warning.json')[f'{server.id}'][f'{user.id}']['count']
            b = dataIO.load_json('data/mod/warning.json')[f'{server.id}']['all']
            em.add_field(name=data['6'], value=f'{a}/{b}')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await ctx.guild.get_channel(int(log)).send(embed=em)

def check_folder():
    if not os.path.exists('data/mod'):
        print('data/mod 풀더생성을 완료하였습니다!')
        os.makedirs('data/mod')

def check_file():
    data = {}
    f = "data/mod/settings.json"
    g = 'data/mod/warning.json'
    h = 'data/mod/welcome.json'
    if not dataIO.is_valid_json(f):
        print("data/mod/settings.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)
    if not dataIO.is_valid_json(g):
        print("data/mod/warning.json 파일생성을 완료하였습니다!")
        dataIO.save_json(g,
                         data)
    if not dataIO.is_valid_json(h):
        print("data/mod/welcome.json 파일생성을 완료하였습니다!")
        dataIO.save_json(h,
                         data)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Mod(bot))
