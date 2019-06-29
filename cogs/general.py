import discord
import datetime
import inspect
import os
import time
from discord import Spotify
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from discord import VoiceRegion
from discord import Game
import subprocess
import sys
import time

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, user:discord.Member=None):
        author = ctx.message.author
        if not user:
            user = author
        else:
            pass
        roles = [role.mention for role in user.roles]
        if roles:
            for page in roles:
                lol = ', '.join(roles)     
        else:
            lol = '없음'
        for activity in user.activities:
            if isinstance(activity, Spotify or Game):
                if isinstance(activity, Spotify):            
                    yee = "Spotify에서 {}의  {} 노래 듣는중".format(activity.artist, activity.title)
                else:
                    yee = None
            else:
                yee = None
        created_on = user.created_at.strftime("%Y-%m-%d %H:%M")
        joined_on = user.joined_at.strftime("%Y-%m-%d %H:%M")
        if yee:
            em = discord.Embed(colour=author.colour, title='USERINFO || 유저정보', description=yee, timestamp=datetime.datetime.utcnow())
        else:
            em = discord.Embed(colour=author.colour, title='USERINFO || 유저정보')
        em.add_field(name='유저 태그', value=user)
        em.add_field(name='**ID**', value=user.id, inline=False)
        if user.activity.name == None:
            pass
        elif user.activity.name == 'Spotify':
            pass
        else:
            em.add_field(name='활동', value=user.activity.name, inline=False)
        em.add_field(name='가입 한 날짜', value=created_on, inline=False)
        em.add_field(name='이 서버 들어온 날짜', value=joined_on, inline=False)
        if len(lol) > 1024:
            em.add_field(name='역할', value='1024자를 넘겨서 더이상 출력이 불가합니다!')
        else:
            em.add_field(name='역할', value=lol)

        if user.avatar_url:
            em.set_thumbnail(url=user.avatar_url)
        else:
            pass
        try:
            await ctx.send(author.mention)
            await ctx.send(embed=em)
        except Exception as e:
            print(e)

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        author = ctx.author
        server = ctx.author.guild
        created_at = server.created_at.strftime("%Y-%m-%d %H:%M")
        level = dataIO.load_json('server_level/level.json')["{}".format(server.verification_level)]
        region = dataIO.load_json('region/region.json')["{}".format(server.region)]
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
        em.add_field(name='서버 생성일', value=created_at, inline=False)
        if len(lol) > 1024:
            em.add_field(name='역할', value='1024자를 넘겨서 더이상 출력이 불가합니다!', inline=False)
        else:
            em.add_field(name='역할', value=lol, inline=False)
        em.add_field(name='서버 인원', value="**{} 명**".format(len(server.members)))
        await ctx.send(embed=em)
    
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        author = ctx.author
        channel = ctx.message.channel
        t1 = time.perf_counter()
        channel.typing(channel)
        t2 = time.perf_counter()
        em = discord.Embed(colour=author.colour)
        em.add_field(name='**퐁!**', value='디스코드 API 핑 {}ms'.format(round((t2-t1)*1000)))
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(general(bot))
