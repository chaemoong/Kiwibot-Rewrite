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
from pymongo import MongoClient
import settings
set = settings.set()
try:
    client = MongoClient(host=set.ip, port=set.port, username=set.user, password=set.pwd, authSource=set.auth)    
    db = client['chaemoong']['mod']
    lang = client['chaemoong']['mod.language'].find_one
except:
    print('Mod Cogs에서 MongoDB에 연결하지 못했습니다!')

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
        self.welcome2 = dataIO.load_json(self.welcome)

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

    @commands.command(no_pm=True, name='clear', description='The messages deleting command! | 메시지를 삭제하는 명령어입니다!', aliases=['칟ㅁㄱ', '청소', 'cjdth'])
    @commands.check(administrator)
    async def clear(self, ctx, count:int=None):
        try:
            await ctx.channel.purge(limit=count+1)
        except:
            return await ctx.send('봇에 권한이 없습니다! 권한을 추가해주세요! | No permission')
        return await ctx.send(f'{count} 개의 메시지를 지웠습니다!')

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
            return await a.edit(content='> 정상적으로 취소되었습니다! | Canceled!')
        if True:
            await a.delete()
            if str(reaction.emoji) == '🇰🇷':
                try:
                    db.language.delete_one({"_id": server.id})
                    db.language.insert_one({"_id": server.id, "language": "ko"})
                except KeyError:
                    db.language.insert_one({"_id": server.id, "language": "ko"})
                return await ctx.send('> 언어가 성공적으로 `한글` 로 설정 되었습니다!')            
            if str(reaction.emoji) == '🇺🇸':
                try:
                    db.language.delete_one({"_id": server.id})
                    db.language.insert_one({"_id": server.id, "language": "en"})
                except KeyError:
                    db.language.insert_one({"_id": server.id, "language": "en"})
                return await ctx.send('> Language has been successfully set as `English`')        
        else:
            return await ctx.send("> 다른 이모지를 추가하지 마세요! | Please don't add another emoji")

    @commands.command(no_pm=True, name='ban', description='It is a user-banning command. | 유저를 벤하는 명령어입니다!', aliases=['ㅠ무', '벤', 'qps', '차단', 'ckeks'])
    @commands.check(administrator)
    async def ban(self, ctx, user:discord.Member=None, *, reason=None):
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        guild = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        guild = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        author = ctx.author
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        author = ctx.author
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        author = ctx.author
        server = ctx.guild
        if user == None:
            user = author
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        num = 0
        for reason in a:
            num += 1
            em.add_field(name=data['7'].format(num), value=reason, inline=False)
        return await ctx.send(embed=em)

    @commands.command(no_pm=True, name='clean', description='It is a user-warnning cleaning command. | 유저의 경고를 삭제하는 명령어입니다!', aliases=['칟무', '경고삭제', 'rudrhtkrwp'])
    @commands.check(administrator)
    async def clean(self, ctx, user:discord.Member=None, *, reason=None):
        author = ctx.author
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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

    @commands.group(no_pm=True, name='welcomeset', description='Commands to set welcome functions! | 환영/퇴장 기능들을 설정하는 명령어입니다!', aliases=['ㅈ디채ㅡㄷㄴㄷㅅ', '웰컴기능설정', 'dnpfzjarlsmdtjfwjd'])
    @commands.check(administrator)
    async def welcomeset(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(colour=discord.Colour.orange(), title='환영기능 설정 | Welcome Funcion Settings', timestamp=datetime.datetime.utcnow())
            em.add_field(name='아래에는 사용 가능한 명령어들입니다!', value='channel - 유저 환영/퇴장 메시지를 보내는 채널을 설정합니다!\nhimsg - 유저 환영 메시지를 설정하는 명령어에욧!\nbyemsg - 유저 퇴장 메시지를 설정하는 명령어에욧!')
            return await ctx.send(ctx.author.mention, embed=em)

    @welcomeset.command(pass_context=True)
    async def channel(self, ctx, channel:discord.TextChannel=None):
        print(ctx)
        author = ctx.author
        server = ctx.guild
        if channel == None:
            return await ctx.send(f'{author.mention}, 채널의 멘션 혹은 ID를 적어주세요!')
        em = discord.Embed(colour=discord.Colour.gold(), title='채널 설정 | CHANNEL SETTINGS', timestamp=datetime.datetime.utcnow())
        em.add_field(name='지정하시려면 ⭕ 취소하리면 ❌에 반응해주세요!', value=f'정말로 {channel.mention} 채널을 환영 메시지 보내는 채널로 지정하실건가요???')
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
            return await a.edit(content='> 시간초과로 인해 취소되었습니다!')
        if True:
            await a.delete()
            em2 = discord.Embed(colour=discord.Colour.gold(), title='채널 설정 | CHANNEL SETTINGS', timestamp=datetime.datetime.utcnow())
            if reaction.emoji == '⭕':
                if self.welcome2.get(f'{server.id}') == None:
                    self.welcome2[str(server.id)] = {}
                self.welcome2[str(server.id)].update({"channel": channel.id})
                dataIO.save_json(self.welcome, self.welcome2)
                em2.add_field(name='성공!', value=f'이제 환영 메시지를 {channel.mention} 채널에 보냅니다!')
                return await ctx.send(author.mention, embed=em2)
            if reaction.emoji == '❌':
                em2.add_field(name='에러!', value='취소되었습니다!')
                return await ctx.send(author.mention, embed=em2)
            else:
                return await ctx.send(f'{author.mention}, 다른 이모지를 추가하지 마세요!')

    @welcomeset.command(pass_context=True)
    async def himsg(self, ctx, *, message=None):
        server = ctx.guild
        author = ctx.author
        em = discord.Embed(colour=discord.Colour.gold(), title='메세지 설정 | MESSAGE SETTINGS', timestamp=datetime.datetime.utcnow())
        if message == None:
            em.add_field(name='메시지를 제대로 적어주세요!', value="예: {0.name} == 들어온 사람의 이름\n{0.mention} == 들어온 사람의 멘션\n{0} == 들어온 사람의 태그")
            return await ctx.send(author.mention, embed=em)
        em.add_field(name='지정하시려면 ⭕ 취소하리면 ❌에 반응해주세요!', value=f'정말로 `{message}` 메시지를 환영 메시지로 지정하실건가요???')
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
            return await a.edit(content='> 시간초과로 인해 취소되었습니다!')
        if True:
            await a.delete()
            em2 = discord.Embed(colour=discord.Colour.gold(), title='메세지 설정 | MESSAGE SETTINGS', timestamp=datetime.datetime.utcnow())
            if reaction.emoji == '⭕':
                if self.welcome2.get(f'{server.id}') == None:
                    self.welcome2[f'{server.id}'] = {}
                self.welcome2[f'{server.id}'].update({"message1": message})
                dataIO.save_json(self.welcome, self.welcome2)
                em2.add_field(name='성공!', value=f'이제 환영 메시지를 {message}로 설정하였습니다!')
                return await ctx.send(author.mention, embed=em2)
            if reaction.emoji == '❌':
                em2.add_field(name='에러!', value='취소되었습니다!')
                return await ctx.send(author.mention, embed=em2)
            else:
                return await ctx.send(f'{author.mention}, 다른 이모지를 추가하지 마세요!')

    @welcomeset.command(pass_context=True)
    async def byemsg(self, ctx, *, 메시지=None):
        author = ctx.author
        server = ctx.guild.id
        em = discord.Embed(colour=discord.Colour.gold(), title='메세지 설정 | MESSAGE SETTINGS', timestamp=datetime.datetime.utcnow())
        if 메시지 == None:
            em.add_field(name='메시지를 제대로 적어주세요!', value="예: {0.name} == 들어온 사람의 이름\n{0.mention} == 들어온 사람의 멘션\n{0} == 들어온 사람의 태그")
            return await ctx.send(author.mention, embed=em)
        em.add_field(name='지정하시려면 ⭕ 취소하리면 ❌에 반응해주세요!', value=f'정말로 `{메시지}` 메시지를 퇴장 메시지로 지정하실건가요???')
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
            return await a.edit(content='> 시간초과로 인해 취소되었습니다!')
        if True:
            em2 = discord.Embed(colour=discord.Colour.gold(), title='메세지 설정 | MESSAGE SETTINGS', timestamp=datetime.datetime.utcnow())
            if reaction.emoji == '⭕':
                if self.welcome2.get(f'{server}') == None:
                    self.welcome2[f'{server}'] = {}
                self.welcome2[f'{server}'].update({"message2": 메시지})
                dataIO.save_json(self.welcome, self.welcome2)
                em2.add_field(name='성공!', value=f'이제 퇴장 메시지를 {메시지}로 설정하였습니다!')
                return await ctx.send(author.mention, embed=em2)
            if reaction.emoji == '❌':
                em2.add_field(name='에러!', value='취소되었습니다!')
                return await ctx.send(author.mention, embed=em2)
            else:
                return await ctx.send(f'{author.mention}, 다른 이모지를 추가하지 마세요!')

    @commands.group(no_pm=True, name='settings', description='Commands to set administrator functions! | 관리자 기능들을 설정하는 명령어입니다!', aliases=['ㄴㄷㅅ샤ㅜㅎㄴ', '관리자기능설정', 'rhksflwkrlsmdtjfwjd'])
    @commands.check(administrator)
    async def settings(self, ctx):
        author =  ctx.author
        if ctx.invoked_subcommand is None:
            server = ctx.guild
            try:
                asdf = lang({'_id': ctx.guild.id})
                if asdf['language'] == 'ko':
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
            repeat = self.bot.lavalink.players.get(ctx.guild.id).repeat
            if not log: log = data['None']
            if asdfasdf == None:
                volume = '100'
            else:
                volume = asdfasdf
            em = discord.Embed(colour=ctx.author.colour)        
            em.add_field(name=':passport_control:' + data['first'], value=data['embed1'].format(admin, mod, rold))
            em.add_field(name=':newspaper:' + data['second'], value=data['embed2'].format(log))
            em.add_field(name=':musical_note:' + data['third'], value=data['embed3'].format(volume, (data['on'] if repeat else data['off'])))
            em.add_field(name=data['basic']['a'], value=data['basic']['admin'].format(ctx))
            if author.avatar_url:
                em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
            else:
                em.set_footer(text=f'Request By {author}')
            return await ctx.send(author.mention, embed=em)

    @settings.command(pass_context=True)
    async def admin(self, ctx, role:discord.Role=None):
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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

    @settings.command(pass_context=True)
    async def mod(self, ctx, role:discord.Role=None):
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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

    @settings.command(pass_context=True)
    async def log(self, ctx, channel:discord.TextChannel=None):
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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

    @settings.command(pass_context=True)
    async def 욕필터(self, ctx):
        author = ctx.author
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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

    @settings.command(pass_context=True)
    async def role(self, ctx, role:discord.Role=None):
        server = ctx.guild
        try:
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':
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
            asdf = lang({'_id': ctx.guild.id})
            if asdf['language'] == 'ko':

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
        em = discord.Embed(colour=discord.Colour.red())
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
