import os
import sys
import urllib.request
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import json
import asyncio
from discord.utils import get
import settings
set = settings.set()
try:
    client = MongoClient(host=set.ip, port=set.port)
    lang = client['mod'].language.find_one
except:
    print("captcha Cog에서 몽고DB를 연결할 수 없습니다!")

class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error = dataIO.load_json('data/captcha/error.json')
        self.first = dataIO.load_json('data/mod/settings.json')
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'


    @commands.command(no_pm=True, name='verify', description='The verify command! | 인증 명령어입니다!', aliases=['인증', 'ㅍㄷ갸료', 'dlswmd'])
    async def verify(self, ctx):
        """인증 명령어입니다!"""
        server = ctx.guild
        author = ctx.author
        log = dataIO.load_json('data/mod/settings.json')
        asdf = lang({"_id": server.id})
        try:
            if asdf['language'] == 'ko':
                data = dataIO.load_json(self.ko)[ctx.command.name]
            else:
                data = dataIO.load_json(self.en)[ctx.command.name]
        except:
            data = dataIO.load_json(self.en)[ctx.command.name]
        if f'{server.id}' in log:
            try:
                role = get(server.roles, id=log[f'{server.id}']['rold'])
            except KeyError:
                return await ctx.send(data['1'].format(data['role']))
        else:
            return await ctx.send(data['1'].format(data['role']))
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
        try:
            url = "https://openapi.naver.com/v1/captcha/nkey?code=" + code + "&key=" + key + "&value=" + wait.content
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
        except:
            return await author.send(data['10'])
        if(rescode==200):
            response_body = response.read()
            thinking = response_body.decode('utf-8')
        else:
            print("Error Code:" + rescode)
            return await author.send(data['4'].format(rescode, self.error[str(rescode)]))
        a = json.loads(thinking)
        if a['result']:
            await author.send(data['9'])
            roldeee = int(self.first[f'{server.id}']['rold'])
            try:
                return await author.add_roles(get(server.roles, id=roldeee))
            except:
                return await ctx.send('> No Permission or No Find the Role Please contact to Administrator')  
        else:
            return await author.send(data['10'])
                
def check_folder():
    if not os.path.exists('data/captcha'):
        print('data/captcha 풀더생성을 완료하였습니다!')
        os.makedirs('data/captcha')
    if not os.path.exists('data/mod'):
        print('data/mod 풀더생성을 완료하였습니다!')
        os.makedirs('data/mod')

def check_file():
    data = {
    "400": "Unissued image (이미지 발급을 하지 않음)",
    "403": "Invalid key. (키가 만료되거나 없는 키)",
    "500": "System error. (시스템 오류)"
    }
    f = "data/captcha/error.json"
    dataasdf = {}
    fg = "data/mod/settings.json"
    if not dataIO.is_valid_json(fg):
        print("data/mod/settings.json 파일생성을 완료하였습니다!")
        dataIO.save_json(fg,
                         dataasdf)
    elif not dataIO.is_valid_json(f):
        print("error.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Captcha(bot))
