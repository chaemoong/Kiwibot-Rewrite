import os
import sys
import urllib.request
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import json
import asyncio
from discord.utils import get

class captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error = dataIO.load_json('data/captcha/error.json')
        self.first = dataIO.load_json('data/mod/settings.json')
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'


    @commands.command(no_pm=True, name='verify', description='The verify command! | 인증 명령어입니다!', aliases=['인증', 'ㅍㄷ갸료', 'dlswmd'])
    async def verify(self, ctx):
        """인증 명령어입니다!"""
        channel = ctx.channel
        server = ctx.guild
        author = ctx.author
        log = self.first
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{server.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if f'{server.id}' in log:
            if 'rold' in log[f'{server.id}']:
                role = get(server.roles, id=log[f'{server.id}']['rold'])
            else:
                return await ctx.send(data['1'].format(data['role']))
        else:
            return await ctx.send(data['1'].format(data['role']))
        if channel.id == log[f'{server.id}']['channel']:
            pass
        else:
            return await ctx.send(data['2'])
        if get(server.roles, id=role) in author.roles:
            return await ctx.send(data['3'])
        client_id = "3VuiEnBYyTLIRMOHWDLq"
        client_secret = "LFF_fdqvUL"
        code = "0"
        url = "https://openapi.naver.com/v1/captcha/nkey?code=" + code
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
        else:
            print("Error Code:" + rescode)
            return await author.send(data['4'].format(rescode, self.error[str(rescode)]))
        v1 = response_body.decode('utf-8')
        key = json.loads(v1)['key']
        url = "https://openapi.naver.com/v1/captcha/ncaptcha.bin?key=" + key
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            with open('captcha.jpg', 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)
            return await author.send(data['4'].format(rescode, self.error[str(rescode)]))
        code = "1"
        em = discord.Embed(colour=author.colour)
        em = discord.Embed(colour=author.colour, title=data['5'])
        await ctx.send(embed=em)
        em2 = discord.Embed(colour=author.colour)
        em2.add_field(name=data['6'].format(ctx.guild.name), value=data['7'])
        await author.send(file=discord.File(open("captcha.jpg", "rb")), embed=em2)
        try:
            def check(message):
                return message.channel.id == author.dm_channel.id
            wait = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await author.send(data['8'])
        url = "https://openapi.naver.com/v1/captcha/nkey?code=" + code + "&key=" + key + "&value=" + wait.content
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            thinking = response_body.decode('utf-8')
        else:
            print("Error Code:" + rescode)
            return await author.send(data['4'].format(rescode, self.error[str(rescode)]))
        a = json.loads(thinking)
        if a['result']:
            await author.send(data['9'])
            return await author.add_roles(get(server.roles, id=self.first[f'{server.id}']['rold']))
        else:
            return await author.send(data['10'])
                
def setup(bot):
    bot.add_cog(captcha(bot))
