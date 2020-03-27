"""coding: UTF-8, coding by: discordtag: chaemoong#9454"""
import discord
import aiohttp
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import os

class Post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.company = dataIO.load_json('data/post/company_name.json')
        self.smart = dataIO.load_json('data/post/smart.json')
        self.apikey = dataIO.load_json('data/post/apikey.json')

    async def is_owner(ctx):
        return ctx.author.id == 431085681847042048

    @commands.command(no_pm=True, name='택배', description='The order to inquire parcels! | 택배를 조회하는 명령어입니다!', aliases=['xorqo', 'post', 'ㅔㅐㄴㅅ'])
    async def 택배(self, ctx, company_name=None, tb_number:str=None):
        api = "HMffQXQBajeVUjTuAcc4Ag"
        if company_name == None or not self.company.get(company_name):
            await ctx.send('택배회사를 제대로 적어주셔야 되요!\n그리고 편의점 택배는 대부분 CJ대한통운, 롯데택배, 한진택배이니 참고해주세요!')
            return
        for name in self.smart['Company']:
            if name['Name'] == company_name:
                code = name.get('Code')
                break
            else:
                code = None
        if code == None: return await ctx.send('택배회사를 제대로 적어주셔야 되요!\n그리고 편의점 택배는 대부분 CJ대한통운, 롯데택배, 한진택배이니 참고해주세요!')
        if tb_number == None:
            await ctx.send('송장번호를 적어주셔야 되요!')
            return
        try:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://info.sweettracker.co.kr/api/v1/trackingInfo?t_key={api}&t_code={code}&t_invoice={tb_number}") as response:
                        data = await response.json()      
                        if data.get('code') == '105':
                            raise          
            except:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://apis.tracker.delivery/carriers/{self.company.get(company_name)}/tracks/{tb_number}") as response:
                        data = await response.json()             
            try:
                em = discord.Embed(colour=ctx.author.colour, title=f':truck: 택배 조회 ({data["state"]["text"]})')
            except: 
                smartdeliverycode = {"1": "배송준비중", "2": "집화완료", "3": "배송중", "4": "배달지도착", "5": "배송출발", "6":"배송완료"}
                em = discord.Embed(colour=ctx.author.colour, title=f':truck: 택배 조회 ({smartdeliverycode.get(str(data["level"]))})')
            try:
                em.add_field(name='보내는 사람 | 받는사람', value=f"`{data['from']['name']} | {data['to']['name']}`")     
            except:
                em.add_field(name='보내는 사람 | 받는사람', value=f"`{data['senderName'][:1] + ('**' if len(data['senderName']) > 2 else '*')} | {data['receiverName'][:1] + ('**' if len(data['receiverName']) > 2 else '*')}`")      
            try:
                em.add_field(name='물품 이름', value=f"{data['itemName']}")     
            except: pass
            other = []
            ymd = []
            smart = data.get('trackingDetails')
            if smart == None:
                smart = data.get('progresses')
            for item in smart:
                if smart == data.get('progresses'):
                    a = item.get('time')
                    if a:
                        if not a[:10] in other: other.append(a[:10])
                        time = a[11:16]
                    else:
                        time = ''                    
                    if item.get('location'):
                        location = item.get('location').get('name')
                    else:
                        location = ''               
                    if item.get('description'):
                        desc = item.get('description')
                    else:
                        desc = ''
                    ymd.append(f'{a[:10]} [{location}] **{time}** - {desc}')
                else:
                    a = item.get('timeString')
                    if a:
                        if not a[:10] in other: other.append(a[:10])
                        time = a[11:16]
                    else:
                        time = ''                    
                    if item.get('where'):
                        location = item.get('where')
                    else:
                        location = ''               
                    if item.get('kind'):
                        desc = item.get('kind').replace('\n', ' ')
                    else:
                        desc = ''
                    ymd.append(f'{a[:10]} [{location}] **{time}** - {desc}')
            for asdf in other:    
                real = []
                for cd in ymd:
                    if cd.startswith(asdf):
                        real.append(cd[11:])
                em.add_field(name=asdf, value='\n'.join(real), inline=False)
            em.set_footer(text=f'Request by: {ctx.author} || Helped By: {self.bot.get_user(351613953769603073)}\n본 정보는 스마트택배 혹은 delivery-tracker 에서 제공받는 정보로,\n실제 배송상황과 다를 수 있습니다.')
            await ctx.send(embed=em)
        except Exception as e:
            a = self.bot.get_user(431085681847042048)
            em = discord.Embed(colour=discord.Colour.red())
            em.add_field(name='404!', value='API가 이상이 있거나 어떠한 오류가 발생하였습니다!\n빠른 시일내로 고치도록 하겠습니다!')
            await ctx.send(embed=em)
            await a.send(f'`{ctx.command}` 명령어에 오류가 발생하였습니다!\n```\n{type(e)} {e}\n```')

    @commands.command(no_pm=True, name='apikey', description='스윗트래커 API키가 만료 되었을때 사용하는 명령어 입니다!', aliases=['메ㅑㅏ됴'])
    @commands.check(is_owner)
    async def key(self, ctx, *, key=None):
        if key == None:
            return await ctx.send('API키를 적어주세요!')
        await ctx.message.delete()
        a = {'key': key}
        dataIO.save_json("data/post/apikey.json", a)
        return await ctx.send('API 키가 업데이트 되었습니다!')


def check_folder():
    if not os.path.exists('data/post'):
        print('data/post 풀더생성을 완료하였습니다!')
        os.makedirs('data/post')

def check_file():
    data = {
   "DHL": "de.dhl",
   "천일택배": "kr.chunilps",
   "CJ대한통운": "kr.cjlogistics",
   "CU택배": "kr.cupost",
   "GS택배": "kr.cvsnet",
   "CWAY": "kr.cway",
   "대신택배": "kr.daesin",
   "우체국택배": "kr.epost",
   "한의사랑택배": "kr.hanips",
   "한진택배": "kr.hanjin",
   "합동택배": "kr.hdexp",
   "홈픽": "kr.homepick",
   "한서호남택배": "kr.honamlogis",
   "일양로지스": "kr.ilyanglogis",
   "경동택배": "kr.kdexp",
   "건영택배": "kr.kunyoung",
   "로젠택배": "kr.logen",
   "롯데택배": "kr.lotte",
   "SLX": "kr.slx",
   "TNT": "nl.tnt",
   "EMS": "un.upu.ems",
   "FEDEX": "us.fedex",
   "UPS": "us.ups",
   "USPS": "us.usps"
}
    empty = {}
    f = "data/post/company_name.json"
    if not dataIO.is_valid_json(f):
        print("company_name.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)
    g = "data/post/apikey.json"
    if not dataIO.is_valid_json(g):
        print("apikey.json 파일생성을 완료하였습니다!")
        dataIO.save_json(g,
                         empty)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Post(bot))
