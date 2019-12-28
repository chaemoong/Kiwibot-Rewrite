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


class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = dataIO.load_json('data/general/status.json')
        self.author = dataIO.load_json('data/general/author.json')
        self.data = dataIO.load_json('data/general/stat.json')
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'


    @commands.command()
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
        em.add_field(name=data['10'], value=user.created_at.strftime(data['time'].encode('unicode-escape').decode()).encode().decode('unicode-escape'), inline=False)
        em.add_field(name=data['13'], value=user.joined_at.strftime(data['time'].encode('unicode-escape').decode()).encode().decode('unicode-escape'), inline=False)
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

    @commands.command(pass_context=True)
    async def 멜론(self, ctx):
        """멜론 차트를 뽑는 명령어입니다!"""
        server = ctx.guild.id
        yee = dataIO.load_json(self.setting)
        try:
            if yee[f'{server}']['language'] == 'ko':
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

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        author = ctx.author
        server = ctx.author.guild
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        a = server.created_at.strftime(data['time'].encode('unicode-escape').decode()).encode().decode('unicode-escape')
        level = dataIO.load_json('server_level/level.json')[f"{server.verification_level}"]
        region = dataIO.load_json('region/region.json')[f"{server.region}"]
        roles =  [role.mention for role in server.roles]
        if roles:
            for page in roles:
                lol = ', '.join(roles)     
        else:
            lol = '없음'
        em=discord.Embed(colour=author.colour, title='SERVERINFO || 서버정보', timestamp=datetime.datetime.utcnow(), description=level)
        em.add_field(name='서버 이름', value=server.name, inline=False)
        em.add_field(name="`ID`", value=server.id, inline=False)
        em.add_field(name='서버 위치', value=region, inline=False)
        em.add_field(name='서버 생성일', value=a, inline=False)
        em.add_field(name='서버 주인', value=server.owner.mention)
        if len(lol) > 1024:
            em.add_field(name='역할', value='1024자를 넘겨서 더이상 출력이 불가합니다!', inline=False)
        else:
            em.add_field(name='역할', value=lol, inline=False)
        em.add_field(name='서버 인원', value="**{} 명**".format(len(server.members)))
        em.set_footer(text='Request By: {}'.format(author))
        if author.avatar_url:
            em.set_thumbnail(url=author.avatar_url)
        else:
            pass
        await ctx.send(author.mention, embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def 화공(self, ctx):
        """통화방에서 화면공유를 도와주는 명령어입니다!"""
        author = ctx.author
        server = author.guild
        em = discord.Embed(colour=author.colour, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f'Request By: {author}')
        try:
            a = author.voice.channel
            url = f"https://discordapp.com/channels/{server.id}/{a.id}"
            em.add_field(name='화면 공유', value=f'**서버: {server.name}\n음성 채널: [{a.name}]({url})**')
            await ctx.send(embed=em)
        except AttributeError:
            await ctx.send('먼저 음성 채널에 접속해주세요!')
            
    @commands.command(pass_context=True, no_pm=True)
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
        em2 = discord.Embed(title='핑! 퐁!', colour=Color, timestamp=datetime.datetime.utcnow())
        em2.add_field(name=f"**디스코드 API: `{ping}ms`**", value=f'메세지: `{msgping}ms`')
        if author.avatar_url:
            em2.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em2.set_footer(text=f'Request By {author}')
        await msg.edit(embed=em2)

    @commands.command(pass_context=True, no_pm=True)
    async def chinobot(self, ctx):
        """ChinoBot의 API 정보를 불러와요!"""
        a = await ctx.send('잠시만 기달려주세요!')
        author = ctx.author
        url = "http://siru.ga/api/main_module"
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
        em.add_field(name='치노봇의 핑', value=str(ping) + 'ms', inline=False)
        em.add_field(name='치노봇의 유저수', value=str(user) + '명', inline=False)
        em.add_field(name='치노봇의 서버수', value=str(server) + '개', inline=False)
        em.add_field(name='치노봇의 업타임 시간', value=uptime)
        em.set_thumbnail(url=chino.avatar_url)
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        await a.delete()
        await ctx.send(embed=em)

    
def setup(bot):
    bot.add_cog(general(bot))
