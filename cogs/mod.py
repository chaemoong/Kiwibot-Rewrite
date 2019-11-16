import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils.dataIO import dataIO
import json
import asyncio
import datetime

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ang = 'data/mod/settings.json'
        self.data = dataIO.load_json(self.ang)
        self.cass = 'data/mod/case.json'
        self.case = dataIO.load_json(self.cass)

    async def owner(ctx):
        ctx.author.id == 431085681847042048

    async def admin(ctx):
        if ctx.author.id == 431085681847042048:
            return True
        elif ctx.author.guild_permissions.administrator == True:
            return True
    
    @commands.command(pass_context=True, no_pm=True)
    @commands.check(owner)
    async def asdf(self, ctx):
        return await self.send_cmd_help(ctx)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(admin)
    @commands.has_permissions(administrator=True)
    async def language(self, ctx, language=None):
        """봇의 언어를 설정하는 명령어 입니다!"""
        with open(self.ang, encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        server = ctx.author.guild
        author = ctx.author
        if language:
            if language == 'ko_kr' or language == 'ko' or language == '한국어':
                if not f'{server.id}' in json_data:
                    self.data[f'{server.id}'] = {}
                    dataIO.save_json(self.ang,
                                self.data)                
                try:
                    if self.data[f'{server.id}']['languages'] == 'ko':
                        em=discord.Embed(colour=author.colour)
                        em.add_field(name='오류! | ERROR', value='언어가 이미 한국어로 설정 되어있습니다!\nLanguage is already setting to `Korean`')
                        return await ctx.send(embed=em)
                except KeyError:
                    del self.data[f'{server.id}']['languages']
                    self.data[f'{server.id}'] = {}
                    self.data[f'{server.id}'].update({"languages": 'ko'})
                    dataIO.save_json(self.ang,
                                self.data)                
                em=discord.Embed(colour=author.colour)
                em.add_field(name='완료! | Finished!', value='언어가 한국어로 설정 되었습니다!\nSucceeds set language to `English`')
                await ctx.send(embed=em)

            elif language == 'en_us' or language == 'en' or language == '영어':
                if not f'{server.id}' in json_data:
                    self.data[f'{server.id}'] = {}
                    dataIO.save_json(self.ang,
                                self.data)                
                try:
                    if self.data[f'{server.id}']['languages'] == 'en':
                        em=discord.Embed(colour=author.colour)
                        em.add_field(name='오류! | ERROR', value='언어가 이미 영어로 설정 되어있습니다!\nLanguage is already setting to `English`')
                        return await ctx.send(embed=em)
                except KeyError:
                    del self.data[f'{server.id}']['languages']
                    self.data[f'{server.id}'] = {}
                    self.data[f'{server.id}'].update({"languages": 'en'})
                    dataIO.save_json(self.ang,
                                self.data)                
                em=discord.Embed(colour=author.colour)
                em.add_field(name='완료! | Finished!', value='언어가 영어로 설정 되었습니다!\nSucceeds set language to `English`')
                await ctx.send(embed=em)
            else:
                em=discord.Embed(colour=author.colour)
                em.add_field(name='Language Settings | 언어설정', value='This command is Language Settings command!\nLanguage Example: ko_kr, en_us\n언어 선택 명령어입니다!\n언어는 ko_kr, en_us 으로 총 2개입니다!')
                await ctx.send(embed=em)
        else:
            em=discord.Embed(colour=author.colour)
            em.add_field(name='Language Settings | 언어 설정', value='This command is Language Settings command!\nLanguage Example: ko_kr, en_us\n언어 선택 명령어입니다!\n언어는 ko_kr, en_us 으로 총 2개입니다!')
            await ctx.send(embed=em)


    async def send_cmd_help(self, ctx):
        c = self.bot.get_channel(ctx.message.channel.id)
        em = discord.Embed(colour=ctx.author.colour)
        em.add_field(name='그 명령어는 없는 명령어입니다!', value='`{0.prefix}help` 으로 확인하세요!'.format(ctx))
        em.set_footer(text='제대로 작성하였는지 확인해주시고 사용해주세요!')
        return await c.send(embed=em)


def setup(bot):
    bot.add_cog(Mod(bot))
