import discord
import aiohttp
from discord.ext import commands
from cogs.utils.dataIO import dataIO

class post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.company = dataIO.load_json('data/post/company_name.json')

    @commands.command(pass_context=True, no_pm=True)
    async def 택배(self, ctx, company_name, tb_number:str):
        if not company_name or not self.company.get(company_name): return await ctx.send('택배회사 적어 시발룐아')
        if not tb_number: return await ctx.send('송장번호도 제대로 적으세여^^')
        
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


def setup(bot):
    bot.add_cog(post(bot))
