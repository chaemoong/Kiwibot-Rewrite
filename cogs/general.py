"""coding: UTF-8, coding by: discordtag: chaemoong#9454"""
import discord
import datetime
import inspect
import os
import time
from pytz import timezone, utc
from discord import Spotify
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from discord import Game
import subprocess
import sys
import time
import json
import random
from random import choice
import aiohttp
from bs4 import BeautifulSoup
import requests
from enum import Enum
import asyncio
from discord.utils import get

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = dataIO.load_json('data/general/status.json')
        self.author = dataIO.load_json('data/general/author.json')
        self.data = dataIO.load_json('data/general/stat.json')
        self.asdf = 'data/general/money.json'
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'
        self.choice = [True, False]

    @commands.command(no_pm=True, name='돈', description='The money command! | 돈 명령어입니다!', aliases=['money', 'ㅡㅐㅜ됴', 'ehs'])
    async def 돈(self, ctx, user:discord.Member=None):
        author = ctx.author
        if user is None:
            user = author
        asdf = dataIO.load_json(self.asdf)
        try:
            a = asdf.get(str(user.id)).get('money')
        except:
            a = '0'
        em = discord.Embed(colour=author.colour, title='돈', description=f'\n\n`{user.name}`님의 돈은 {a} 키위 있습니다!')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await ctx.send(author.mention, embed=em)

    @commands.command(no_pm=True, name='level', description='It command is checking level! | 레벨을 확인하는 명령어입니다!', aliases=['fpqpf', '레벨', 'ㅣㄷㅍ디'])
    async def level(self, ctx, user:discord.Member=None):
        author = ctx.author
        if user is None:
            user = author
        asdf = dataIO.load_json('level.json')
        a = asdf.get(str(user.id)).get('level')
        em = discord.Embed(colour=author.colour, title='레벨', description=f'\n\n`{user}`님의 레벨은 {a} 레벨입니당!')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await ctx.send(author.mention, embed=em)

    @commands.command(no_pm=True, name='돈받기', description='The money taking command! | 돈받는 명령어입니다!', aliases=['ehsqkerl'])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def 돈받기(self, ctx):
        author = ctx.author
        asdf = dataIO.load_json(self.asdf)
        a = asdf.get(str(author.id))
        if a == None:
            asdf[str(author.id)] = {}
        if asdf[str(author.id)].get('money') == None:
            asdf[str(author.id)].update({'money': 0})
        bb = asdf[str(author.id)].get('money')
        choice = random.choice(self.choice)
        if choice == True:
            c = bb + 3000
            await ctx.send(f'> 당신의 돈은 제가 기부니가 좋아져서 2000키위 에서 1000키위 더 얹어서 총 {c} 키위가 되었습니다!')
        elif choice == False:
            c = bb + 2000
            await ctx.send(f'> 당신의 돈은 제가 기부니가 엄청 좋아지지 않아서 그냥 2000키위만 드려서 총 {c} 키위가 되었습니다!')
        asdf[str(author.id)].update({'money': c})
        dataIO.save_json(self.asdf, asdf)
    
    @commands.command(no_pm=True, name='올인', description='The allin command! | 올인 명령어입니다!', aliases=['dhfdls', 'allin', '미ㅣㅑㅜ'])
    async def 올인(self, ctx):
        author = ctx.author
        asdf = dataIO.load_json(self.asdf)
        try:
            a = asdf.get(str(author.id))
            b = a.get('money')
        except:
            return await ctx.send(f'> 당신은 돈이 없습니다! `{ctx.prefix}돈받기` 명령어로 돈을 받아보세요!')
        if b == 0:
            return await ctx.send(f'> 당신은 돈이 없습니다! `{ctx.prefix}돈받기` 명령어로 돈을 받아보세요!')
        dfdf = await ctx.send('> 정말 올인을 하실꺼에요?\n~~탕진하다 다 잃으시면 배상 안해드립니다!~~\n> 올인을 하시려면 ⭕ 이모지에 반응해주세요!')
        await dfdf.add_reaction('⭕')
        def check(reaction, user):
            if user == ctx.author and str(reaction.emoji) == "⭕": 
                return True 
        try:
            await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await dfdf.edit(content='> 반응을 안해주셔서 취소했어요!')
        choice = random.choice(self.choice)
        if choice == True:
            chaemoong = '성공! '
            c = b * 2
        elif choice == False:
            chaemoong = '실패'
            c = b * 0
        a.update({'money': c})
        dataIO.save_json(self.asdf, asdf)
        em = discord.Embed(colour=author.colour)
        em.add_field(name=f'올인을 {chaemoong}하셨습니다', value=f'당신의 돈은 {c} 키위가 됩니다')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await dfdf.edit(content=author.mention, embed=em)


    @commands.command(no_pm=True, name='userinfo', description='The userinfo command! | 유저정보 명령어입니다!', aliases=['유저정보', 'ㅕㄴㄷ갸ㅜ래', 'dbwjwjdqh'])
    async def userinfo(self, ctx, user:discord.Member=None):
        author = ctx.author
        server = ctx.guild.id
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        self.author[f'{author.id}'] = []
        d = self.author[f'{author.id}']
        if not user:
            user = author
        a = user.web_status
        b = user.mobile_status
        c = user.desktop_status
        roles = [role.mention for role in user.roles]
        if roles:
            for page in roles:
                lol = ', '.join(roles)     
        else:
            lol = '없음'
        if self.client['{}'.format(a)] == 'ok':
            d.append(data["2"])
        else:
            pass
        if self.client['{}'.format(b)] == 'ok':
            d.append(data['3'])
        else:
            pass
        if self.client['{}'.format(c)] == 'ok':
            d.append(data["4"])
        else:
            pass
        if a == 'offline' and b == 'offline' and c == 'offline':
            d.append(data["4"])
        lll = ', '.join(d)
        for activity in user.activities:
            if isinstance(activity, Game):
                yee = data["game"].format(str(activity.name))
            elif isinstance(activity, Spotify):
                yee = data["Spotify"].format(str(activity.artist), str(activity.title))
        try:
            em = discord.Embed(colour=author.colour, title=data['6'], timestamp=datetime.datetime.utcnow(), description=yee)
        except:
            em = discord.Embed(colour=author.colour, title=data['6'], timestamp=datetime.datetime.utcnow(), description=self.data[f'{user.status}'])
        em.add_field(name=data['7'], value=str(user))
        em.add_field(name='**ID**', value=f'{user.id}')
        if len(lol) > 1024:
            em.add_field(name=data['14'], value=data['15'], inline=False)
        else:
            em.add_field(name=data['14'], value=lol, inline=False)
        gf = user.created_at + datetime.timedelta(hours=9)
        fg = user.joined_at + datetime.timedelta(hours=9)
        em.add_field(name=data['10'], value=str(gf) + ' (UTC+9)', inline=False)
        em.add_field(name=data['13'], value=str(fg) + ' (UTC+9)', inline=False)
        try:
            status = user.activities[0].type
            if status == 4:
                em.add_field(name='Custom Status', value=user.activities[0].state)
        except:
            pass
        if lll is None:
            em.add_field(name=data['12'], value=data["1"], inline=False)
        else:
            em.add_field(name=data['12'], value=lll, inline=False)

        em.set_footer(text=f'Request By {author} | Helped by 매리#4633')
        
        if user.avatar_url:
            em.set_thumbnail(url=user.avatar_url)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        await ctx.send(author.mention, embed=em)
        
    @commands.command(no_pm=True, name='melon', description='The melon chart TOP10 command! | 멜론 차트 TOP10 명령어입니다!', aliases=['ㅡ디ㅐㅜ', 'apffhs'])
    async def 멜론(self, ctx):
        """멜론 차트를 뽑는 명령어입니다!"""
        server = ctx.guild.id
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server}']['language'] == 'ko':
                a = '멜론 차트'
            else:
                a = 'Melon Chart'
        except:
            a = 'Melon Chart'
        author = ctx.author
        RANK = 10
    
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://www.melon.com/chart/index.htm', headers = header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')
    
        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        songs = parse.find_all("div", {"class": "ellipsis rank02"})
    
        title = []
        song = []
        em = discord.Embed(colour=author.colour, title=f':melon: {a}')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        em.set_thumbnail(url='https://cdnimg.melon.co.kr/resource/image/web/common/logo_melon142x99.png')
        for t in titles:
            title.append(t.find('a').text)
    
        for s in songs:
            song.append(s.find('span', {"class": "checkEllipsis"}).text)
    
        for i in range(RANK):
            c = int(i+1)
            if int(1) == c:
                if a == 'Melon Chart':
                    b = '1st'
                else:
                    b = '1위'
            if int(2) == c:
                if a == 'Melon Chart':
                    b = '2nd'
            if int(3) == c:
                if a == 'Melon Chart':
                    b = '3rd'
                else:
                    b = '3등'
            else:
                if a == 'Melon Chart':
                    b = f'{c}th'
                else:
                    b = f'{c}등'
            em.add_field(name=f'{b}', value='%s - %s'%(title[i], song[i]), inline=False)
        return await ctx.send(embed=em)

    @commands.command(no_pm=True, name='serverinfo', description='The serverinfo command! | 서버정보 명령어입니다!', aliases=['서버정보', 'ㄴㄷㄱㅍㄷ갸ㅜ래', 'tjqjwjdqh'])
    async def serverinfo(self, ctx):
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
        a = server.created_at.strftime(data['time'].encode('unicode-escape').decode()).encode().decode('unicode-escape')
        level = data[f"{server.verification_level}"]
        region = dataIO.load_json('region/region.json')[f"{server.region}"]
        roles =  [role.mention for role in server.roles]
        if roles:
            for page in roles:
                lol = ', '.join(roles)     
        else:
            lol = data['1']
        em=discord.Embed(colour=author.colour, title=data['2'], timestamp=datetime.datetime.utcnow(), description=level)
        em.add_field(name=data['3'], value=server.name, inline=False)
        em.add_field(name=data['4'], value=server.id, inline=False)
        em.add_field(name=data['5'], value=region, inline=False)
        em.add_field(name=data['6'], value=a, inline=False)
        em.add_field(name=data['7'], value=server.owner.mention)
        if len(lol) > 1024:
            em.add_field(name=data['9'], value=data['8'], inline=False)
        else:
            em.add_field(name=data['9'], value=lol, inline=False)
        em.add_field(name='서버 인원', value="**{} 명**".format(len(server.members)))
        em.set_footer(text='Request By: {}'.format(author))
        if author.avatar_url:
            em.set_thumbnail(url=author.avatar_url)
        else:
            pass
        await ctx.send(author.mention, embed=em)

    @commands.command(no_pm=True, name='screenshare', description='The screenshare command! | 화면공유 명령어입니다!', aliases=['화공', 'ghkrhd', 'ㄴㅊㄱㄷ두놈ㄱㄷ', '화광', 'ghkrhkd'])
    async def screenshare(self, ctx):
        """Helping Another method Screen Share!\n화면공유를 할수 있게 도와주는 명령어에요!"""
        author = ctx.author
        server = author.guild
        try:
            if yee[f'{server.id}']['language'] == 'ko':
                a = '화면 공유'
                b = '**서버: {server.name}\n음성 채널: [{a.name}]({url})**'
                c = '먼저 채팅방에 접속해주세요!'
            else:
                a = 'Screen Share'
                b = '**Server: {server.name}\nVoice Channel: [{a.name}]({url})**'
                c = 'First Join the Voice Channel!'
        except:
            a = 'Screen Share'
            b = '**Server: {}\nVoice Channel: [{}]({})**'
            c = 'First Join the Voice Channel!'

        em = discord.Embed(colour=author.colour, timestamp=datetime.datetime.utcnow())
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        try:
            a = author.voice.channel
            url = f"https://discordapp.com/channels/{server.id}/{a.id}"
            em.add_field(name=a, value=b.format(server.name, a.name, url))
            await ctx.send(embed=em)
        except AttributeError:
            await ctx.send(c)
            
    @commands.command(no_pm=True, name='ping', description='The ping command! | 핑 명령어입니다!', aliases=['핑', 'vld', 'ㅔㅑㅜㅎ'])
    async def ping(self, ctx):
        author = ctx.author
        em = discord.Embed(colour=author.colour, title='PING! || 핑!', timestamp=datetime.datetime.utcnow())
        em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ping = round(self.bot.latency * 1000)
        if ping > 100: Color = 0x95f0ad
        if ping > 200: Color = 0x8ddcf0
        if ping > 300: Color = 0xf0dc8d
        if ping > 400: Color = 0xf0bf95
        if ping > 500: Color = 0xf09595
        if ping > 600: Color = 0xe86666
        before = time.monotonic()
        msg = await ctx.send(embed=em)
        msgping = round((time.monotonic() - before) * 1000)
        em2 = discord.Embed(title='PING! PONG!', colour=Color, timestamp=datetime.datetime.utcnow())
        em2.add_field(name=f"**Discord API: `{ping}ms`**", value=f'Message: `{msgping}ms`')
        if author.avatar_url:
            em2.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em2.set_footer(text=f'Request By {author}')
        await msg.edit(embed=em2)

    @commands.command(no_pm=True, name='chinobot', description='The chinobot API command! | 치노봇에 대한 정보 명령어입니다!', aliases=['치노봇', '초ㅑㅜㅐㅠㅐㅅ', 'clshqht'])
    async def chinobot(self, ctx):
        """Loading ChinoBot's API info!\n치노봇 API를 불러와요!"""
        try:
            if asdf[f'{ctx.guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        a = await ctx.send('잠시만 기달려주세요! | Wait a Second!')
        author = ctx.author
        url = "http://ssh.siru.ga/api/main_module"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                Data = await response.json() 
        ping = Data['ping']
        user = Data['users']
        server = Data['guilds']
        uptime = Data['uptime']
        chino = self.bot.get_user(426722888293548032)
        if ping > 100: Color = 0x95f0ad
        if ping > 200: Color = 0x8ddcf0
        if ping > 300: Color = 0xf0dc8d
        if ping > 400: Color = 0xf0bf95
        if ping > 500: Color = 0xf09595
        if ping > 600: Color = 0xe86666
        em=discord.Embed(colour=Color)
        em.add_field(name=data['1'], value=str(ping) + 'ms', inline=False)
        em.add_field(name=data['2'], value=str(user) + data['3'], inline=False)
        em.add_field(name=data['4'], value=str(server) + data['5'], inline=False)
        em.add_field(name=data['6'], value=uptime)
        em.set_thumbnail(url=chino.avatar_url)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        await a.delete()
        await ctx.send(embed=em)

    @commands.group(no_pm=True, name='translate', description='The translate(papago) API command! | 파파고 명령어입니다!', aliases=['ㅅㄱ무님ㅅㄷ', '파파고', 'papago', 'vkvkrh', 'ㅔ멤해'])
    async def translate(self, ctx):
        """번역 명령어입니다!"""
        if ctx.invoked_subcommand is None:
            await ctx.send('```\n지원하는 언어:\n한국어 : ko\n영어 : en\n일본어 : ja\n중국어: zh-CN\n```')

    
def check_folder():
    if not os.path.exists('data/general'):
        print('data/general 풀더생성을 완료하였습니다!')
        os.makedirs('data/general')

def check_file():
    data = {}
    data2 = {
    "online": "온라인 | ONLINE",
    "dnd": "바쁨 | DND",
    "idle": "자리 비움 | IDLE",
    "offline": "오프라인 | OFFLINE"
    }
    data3 = {
    "online": "ok",
    "dnd": "ok",
    "idle": "ok",
    "offline": "no"
    }
    f = 'data/general/author.json'
    fff = 'data/general/stat.json'
    ddd = 'data/general/status.json'
    asdf = 'data/general/money.json'
    if not dataIO.is_valid_json(f):
        print("author.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)
    elif not dataIO.is_valid_json(fff):
        print("stat.json 파일생성을 완료하였습니다!")
        dataIO.save_json(fff,
                         data2)
    elif not dataIO.is_valid_json(ddd):
        print("status.json 파일생성을 완료하였습니다!")
        dataIO.save_json(ddd,
                         data3)
    elif not dataIO.is_valid_json(asdf):
        print("status.json 파일생성을 완료하였습니다!")
        dataIO.save_json(asdf,
                         data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(general(bot))
