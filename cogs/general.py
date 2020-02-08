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
import urllib.request

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
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def 돈받기(self, ctx):
        author = ctx.author
        asdf = dataIO.load_json(self.asdf)
        a = asdf.get(str(author.id))
        if a == None:
            asdf[str(author.id)] = {}
        if asdf[str(author.id)].get('money') == None:
            asdf[str(author.id)].update({'money': 0})
        bb = asdf[str(author.id)].get('money')
        c = bb + 1000
        em = discord.Embed(colour=discord.Colour.green())
        em.add_field(name='1000키위를 받으셨습니다!', value=f'현재 잔고 `{c}`')
        await ctx.send(embed=em)
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
        await dfdf.delete()
        first = await ctx.send('과연...')
        for i in range(4):
            c = int(i + 1)
            dugu = '두구'
            await first.edit(content= '과연... ' + dugu * c) 
            await asyncio.sleep(1)
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
        return await first.edit(content=author.mention, embed=em)


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
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
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
        if not Color:
            Color = 0x95f0ad
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
        asdf = dataIO.load_json(self.setting)
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
        try:
            em=discord.Embed(colour=Color)
        except:
            em=discord.Embed(colour=0x95f0ad)
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

    @commands.group(no_pm=True, name='cutock', description="Cutock봇 API를 가져오는 명령어입니다! | Get Cutock Bot's API!", aliases=['쳐새차', '쿠톡', 'znxhr'])
    async def cutock(self, ctx):
        """Cutock봇 API를 가져오는 명령어입니다! | Get Cutock Bot's API!"""
        if ctx.invoked_subcommand is None:
            em = discord.Embed(colour=discord.Colour.orange(), title='레벨링 설정 | Leveling Funcion Settings', timestamp=datetime.datetime.utcnow())
            em.add_field(name='아래에는 사용 가능한 명령어들입니다!', value='account - 계좌의 정보를 가져옵니다!')
            return await ctx.send(ctx.author.mention, embed=em)

    @cutock.command(no_pm=True, name='account', description="Cutock봇의 계좌 정보를 가져오는 명령어입니다! | Get Cutock Bot's Account API!", aliases=['ㅁㅊ채ㅕㅜㅅ', '계좌', 'rPwhk'])
    async def account(self, ctx, account=None):
        url = f"http://maryst.iptime.org:90/api/account/{account}"
        try:
            one = await ctx.send('> 조회 중 입니다! 잠시만 기달려주세요!')
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    Data = await response.json()
        except:
            return await one.edit(content='> Cutock API 접속에 실패하였습니다! 잠시후 에 시도 해주세요!')
        if account == None or Data.get('status') == 404:
            return await ctx.send(f'{ctx.author.mention}, 계좌가 존재하지 않습니다!')
        a = {
            "STOCK": "주식통장",
            "SAVING": "저축통장",
            "FREE": "자유입출금통장"
        }
        Type = a[Data['Type']]
        Balance = Data['Balance']
        History = Data['History']
        OWNER = str(self.bot.get_user(Data['UserID']))
        ID = Data['ID']
        Date = Data['Date']
        image = url + '/image'
        if History == []:
            History = '없음'
        if OWNER == None:
            OWNER = '키위봇이 그 유저를 찾기 못했어요!'
        em = discord.Embed(colour=0xffff00, title='Cutock 계좌 안내!')
        em.add_field(name='통장 유형', value=Type, inline=False)
        em.add_field(name='통장 주인', value=OWNER, inline=False)
        em.add_field(name='통장 잔고', value=f'{Balance}원', inline=False)
        em.add_field(name='통장 계좌', value=ID, inline=False)
        em.add_field(name='통장 생성 날짜', value=datetime.datetime.fromtimestamp(int(Date)), inline=False)
        em.add_field(name='통장 이용 내역', value=History, inline=False)
        em.set_image(url=image)
        em.set_footer(text=f'Request by {ctx.author}', icon_url=ctx.author.avatar_url)
        await one.delete()
        return await ctx.send(ctx.author.mention, embed=em)

    @commands.command(name='contact', description='봇 주인한테 연락하는 명령어입니다!', ailases=['채ㅜㅅㅁㅊㅅ', '연락', 'dusfkr'])
    async def contact(self, ctx, *, message=None):
        author = ctx.author
        if message == None:
            return await ctx.send(f'{author.mention}, 메시지를 적어주세요!')
        em = discord.Embed(colour=0xff78cb)
        em.add_field(name='정말로 이 메시지를 보내시겠습니까?', value='이 메시지를 보낼것을 동의하면 봇 관리진에게 이 메시지가 전달됩니다. 그리고 이 모든 말의 책임은 모두 본인에게 있으며, 욕설등의 언행을 하실경우 불이익이 발생될수도 있습니다. 정말 보내시겠습니까?')
        a = await ctx.send(author.mention, embed=em)
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
        await a.delete()
        if True:
            em2 = discord.Embed(colour=discord.Colour.gold(), title='봇 문의 | BOT CONTACT', timestamp=datetime.datetime.utcnow())
            if reaction.emoji == '⭕':
                em2.add_field(name='성공!', value='메시지를 보냈습니다.')
                em3 = discord.Embed(colour=discord.Colour.gold(), title='봇 문의 | BOT CONTACT', timestamp=datetime.datetime.utcnow())
                em3.add_field(name='문의가 들어왔습니다!', value=message)
                if ctx.guild == None:
                    server = 'Direct Message'
                else:
                    server = ctx.guild
                em3.add_field(name='보낸곳, 보낸이', value=f'{server}에서 보내졌으며, {author}({author.id})님이 보내셨습니다!')
                await self.bot.get_user(431085681847042048).send(embed=em3)
                return await ctx.send(author.mention, embed=em2)
            if reaction.emoji == '❌':
                em2.add_field(name='에러!', value='취소되었습니다!')
                return await ctx.send(author.mention, embed=em2)
            else:
                return await ctx.send(f'{author.mention}, 다른 이모지를 추가하지 마세요!')
       

        

    @commands.group(no_pm=True, name='translate', description='The translate(papago) API command! | 파파고 명령어입니다!', aliases=['ㅅㄱ무님ㅅㄷ', '파파고', 'papago', 'vkvkrh', 'ㅔ멤해', '번역', 'qjsdur', 'qjsdurrl', ])
    async def translate(self, ctx):
        """번역 명령어입니다!"""
        a = ['한글 - ko', '영어 - en', '일본어 - ja', '중국어 간체 - zh-CN', '중국어 번체 - zh-TW', '스페인어 - es', '프랑스어 - fr', '러시아어 - ru', '베트남어 - vi', '태국어 - th', '인도네시아어 - id', '독일어 - de', '이탈리아어 - it']
        if ctx.invoked_subcommand is None or ctx.invoked_subcommand in a:
            em = discord.Embed(colour=discord.Colour.green())
            em.add_field(name='지원되는 언어:', value='\n'.join(a), inline=False)
            em.add_field(name='사용방법', value=f'{ctx.prefix}translate en 안녕하세요', inline=False)
            await ctx.send(f'{ctx.author.mention}, 🔴 잘못된 사용 방법입니다!', embed=em)

    @translate.command(no_pm=True, name='en', description='Papago command that translates into English! | 영어로 번역해주는 파파고 명령어입니다!')
    async def en(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='ko', description='Papago command that translates into Korean! | 한글로 번역해주는 파파고 명령어입니다!')
    async def ko(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='ja', description='Papago command that translates into Japanese! | 일본어로 번역해주는 파파고 명령어입니다!')
    async def ja(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='cn', description='Papago command that translates into Korean! zh-CN(China-new)! | 중국어 간체로 번역해주는 파파고 명령어입니다!')
    async def cn(self, ctx, *, message=None):
        return await self.translating(ctx, message, 'zh-CN')

    @translate.command(no_pm=True, name='tw', description='Papago command that translates into zh-TW(China-old)! | 중국어 번체로 번역해주는 파파고 명령어입니다!')
    async def tw(self, ctx, *, message=None):
        return await self.translating(ctx, message, 'zh-TW')

    @translate.command(no_pm=True, name='es', description='Papago command that translates into español(Spain)! | 스페인어로 번역해주는 파파고 명령어입니다!')
    async def es(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='fr', description='Papago command that translates into français(France)! | 프랑스어로 번역해주는 파파고 명령어입니다!')
    async def fr(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='ru', description='Papago command that translates into Русский(Russian)! | 러시아어로 번역해주는 파파고 명령어입니다!')
    async def ru(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='vi', description='Papago command that translates into Tiếng Việt(Vietnam)! | 베트남어 번역해주는 파파고 명령어입니다!')
    async def vi(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='th', description='Papago command that translates into ภาษาไทย(Thailand)! | 태국어로 번역해주는 파파고 명령어입니다!')
    async def th(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='id', description='Papago command that translates into Bahasa Indonesia! | 인도네시아어로 번역해주는 파파고 명령어입니다!')
    async def id(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='de', description='Papago command that translates into Deutsch(German)! | 독일어로 번역해주는 파파고 명령어입니다!')
    async def de(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)

    @translate.command(no_pm=True, name='it', description='Papago command that translates into Italiano(Italia)! | 이탈리아어로 번역해주는 파파고 명령어입니다!')
    async def it(self, ctx, *, message=None):
        return await self.translating(ctx, message, ctx.command.name)


    async def translating(self, ctx, message, target):
        try:
            if message == None:
                return await ctx.send(':x: **번역할 메시지를 적어주세요!**')
            ID = "2I8Gx9HnoSDyGUTBft48"
            SECERT = "oDB5O8NxgI"
            encQuery = urllib.parse.quote(message)
            data = "query=" + encQuery
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",ID)
            request.add_header("X-Naver-Client-Secret",SECERT)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                lang = json.loads(response_body.decode('utf-8'))['langCode']
            else:
                return await ctx.send(f"Error Code: {rescode}")
            client_id = "uRl36eTH0DLB1uqbmKjl"
            client_secret = "eM7loxbRvt"
            encText = urllib.parse.quote(message)
            data = f"source={lang}&target={target}&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                em = discord.Embed(colour=discord.Colour.green())
                em.add_field(name='파파고 번역 결과', value=json.loads(response_body.decode('utf-8'))['message']['result']['translatedText'])
                return await ctx.send(embed=em)
            else:
                return await ctx.send(f"Error Code: {rescode}")
        except urllib.error.HTTPError:
            return await ctx.send("""지원되는 언어는 아래와 같습니다! | Supports Language:```
한국어(ko)-영어(en)
한국어(ko)-일본어(ja)
한국어(ko)-중국어 간체(zh-CN)
한국어(ko)-중국어 번체(zh-TW)
한국어(ko)-스페인어(es)
한국어(ko)-프랑스어(fr)
한국어(ko)-러시아어(ru)
한국어(ko)-베트남어(vi)
한국어(ko)-태국어(th)
한국어(ko)-인도네시아어(id)
한국어(ko)-독일어(de)
한국어(ko)-이탈리아어(it)
중국어 간체(zh-CN) - 중국어 번체(zh-TW)
중국어 간체(zh-CN) - 일본어(ja)
중국어 번체(zh-TW) - 일본어(ja)
영어(en)-일본어(ja)
영어(en)-중국어 간체(zh-CN)
영어(en)-중국어 번체(zh-TW)
영어(en)-프랑스어(fr)
```
""")
        except Exception as e:
            await self.bot.get_user(431085681847042048).send(f'`번역` 명령어에 문제가 발생하였습니다!\n```\n{e}\n```')
            return await ctx.send('관리자 에게 에러 내용을 전달 하였습니다!\n빠른 시일 내에 에러가 고쳐지도록 노력하겠습니다!')

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
