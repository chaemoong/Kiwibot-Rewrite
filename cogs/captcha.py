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

    @commands.command(no_pm=True, name='verify', description='The verify command! | 인증 명령어입니다!', aliases=['인증', 'ㅍㄷ갸료', 'dlswmd'])
    async def verify(self, ctx):
        """인증 명령어입니다!"""
        channel = ctx.channel
        server = ctx.guild
        author = ctx.author
        log = self.first[f'{server.id}']
        if 'channel' in log:
            pass
        else:
            return await ctx.send('> 설정된 캡챠(인증) 채널이 없습니다! 관리자 에게 문의해보세요!\nNo CAPTCHA channel is set! Ask the administrator!')
        try:
            role = self.first[f'{server.id}']['captcha_role']
            if role:
                pass
            else:
                return await ctx.send('> 설정된 캡챠(인증) 역할이 없습니다! 관리자 에게 문의해보세요!\nNo CAPTCHA channel is set! Ask the administrator!')
        except KeyError:
            return await ctx.send('> 설정된 캡챠(인증) 역할이 없습니다! 관리자 에게 문의해보세요!\nNo CAPTCHA channel is set! Ask the administrator!')      
        if not channel.id == log['channel']:
            return await ctx.send('> 인증 명령어는 인증 채널에서 사용해주세요!')
        if get(server.roles, id=role) in author.roles:
            return await ctx.send('> 이미 인증되셨습니다!')
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
            return await author.send(f'{rescode} 오류가 발생했습니다! 오류 내용: {self.error[int(rescode)]}')
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
            return await author.send(f'{rescode} 오류가 발생했습니다! 오류 내용: {self.error[int(rescode)]}')
        code = "1"
        em = discord.Embed(colour=author.colour)
        em = discord.Embed(colour=author.colour, title='DM을 봐주세요!')
        await ctx.send(embed=em)
        em2 = discord.Embed(colour=author.colour)
        em2.add_field(name=f'{ctx.guild.name} 서버에 오신것을 환영합니다!', value='이 기능은 서버의 보안을 위함, 봇 방지로 인하여 캡챠 기능이 생겼습니다!\n아래의 코드를 적어주세요!')
        await author.send(file=discord.File(open("captcha.jpg", "rb")), embed=em2)
        def check(message):
            return message.channel.id == author.dm_channel.id
        try:
            wait = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await author.send('> 캡차가 취소 되었습니다!')
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
            return await author.send(f'{rescode} 오류가 발생했습니다! 오류 내용: {self.error[int(rescode)]}')
        a = json.loads(thinking)
        if a['result']:
            await author.send('> 완료 되었습니다! | Complete!')
            return await author.add_roles(get(server.roles, id=self.first[f'{server.id}']['captcha_role']))
        else:
            return await author.send('> 캡챠키가 올바르지 않습니다! 다시 시도 해주세요! | The CAPTCHA key is invalid! Please try again!')
                
def setup(bot):
    bot.add_cog(captcha(bot))
