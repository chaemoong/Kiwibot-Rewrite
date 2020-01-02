import discord
import aiohttp
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import os

class post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.company = dataIO.load_json('data/post/company_name.json')

    @commands.command(no_pm=True, name='택배', description='The order to inquire parcels! | 택배를 조회하는 명령어입니다!', aliases=['xorqo', 'post', 'ㅔㅐㄴㅅ'])
    async def 택배(self, ctx, company_name=None, tb_number:str=None):
        if company_name == None or not self.company.get(company_name):
            await ctx.send('택배회사를 제대로 적어주셔야 되요!\n그리고 편의점 택배는 대부분 CJ대한통운, 롯데택배, 한진택배이니 참고해주세요!')
            return
        if tb_number == None:
            await ctx.send('송장번호를 적어주셔야 되요!')
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://apis.tracker.delivery/carriers/{self.company.get(company_name)}/tracks/{tb_number}") as response:
                    data = await response.json()
            try:
                d = data['from']['time'][:10]
            except:
                return await ctx.send('송장번호가 존재하지 않거나 정보가 없는 송장번호입니다!')
            em = discord.Embed(colour=ctx.author.colour, title=f':truck: 택배 조회 ({data["state"]["text"]})')
            em.add_field(name='보내는 사람 | 받는사람', value=f"`{data['from']['name']} | {data['to']['name']}`")
            try:
                e = data['to']['time'][:10]
                em.add_field(name='보낸 시간 | 받은 시각', value=f'{d} | {e}')
            except:
                em.add_field(name='보낸 시각', value=f'{d}') # 이부분 데이터 형식을 모르겠어서 못고침
            
            Text = []
            for item in data['progresses']:
                if item.get('time'):
                    time = item.get('time')[:10] + ' ' + item.get('time')[11:19]
                else:
                    time = ''
                
                if item.get('status') and item.get('status').get('text'):
                    status = item.get('status').get('text')
                else:
                    status = ''
                    
                if item.get('location'):
                    location = item.get('location').get('name')
                else:
                    location = ''
                    
                if item.get('description'):
                    desc = item.get('description')
                else:
                    desc = ''
                
                Text.append(f'{location} - {status} {desc}\n**{time}** (UTC)')
            
                
            em.add_field(name='현황', value='\n'.join(Text), inline=False)
            em.set_footer(text=f'Request by: {ctx.author} || Helped By: {self.bot.get_user(351613953769603073)}')
            await ctx.send(embed=em)
        except Exception as e:
            a = self.bot.get_user(431085681847042048)
            em = discord.Embed(colour=discord.Colour.red())
            em.add_field(name='404!', value='API가 이상이 있거나 어떠한 오류가 발생하였습니다!\n빠른 시일내로 고치도록 하겠습니다앗!')
            await ctx.send(em)
            await a.send(f'`{ctx.command}` 명령어에 오류가 발생하였습니다!\n```\n{e}\n```')


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
    f = "data/post/company_name.json"
    if not dataIO.is_valid_json(f):
        print("company_name.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(post(bot))
