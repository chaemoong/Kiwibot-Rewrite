try:
    import discord
except ModuleNotFoundError:
    os.system('pip install -r requirements.txt')
    import discord
import asyncio
import os
import sys
from discord.ext import commands
import random
import json
from discord.ext.commands import AutoShardedBot as a
from os import listdir
from os.path import isfile, join
import traceback
from cogs.utils.dataIO import dataIO
import time
import datetime
import settings
sett = settings.set()
bot = a(command_prefix=sett.first)


@bot.event
async def on_ready():
    print("=" * 50)
    print('{0.user} 계정에 로그인 하였습니다!'.format(bot))
    print("=" * 50)
    bot.load_extension('music')


@bot.before_invoke
async def before_any_command(ctx):
    try:
        if ctx.author.id == 431085681847042048:
            return
        blacklist = dataIO.load_json('blacklist.json')
        if str(ctx.author.id) in blacklist['blacklist']:
            raise commands.CommandNotFound
    except KeyError:
        return

async def playing():
    await bot.wait_until_ready()

    status = ['도움말은 c!help으로 받을 수 있어요!', f'{len(bot.guilds)} SERVERS | {len(set(bot.get_all_members()))} USERS', '키위봇은 꾸준히 성장중이에요!', f'{len(bot.guilds)} 서버 감사합니다!']

    while not bot.is_closed():
        for i in status:
            await bot.change_presence(status=discord.Game(i))
            await asyncio.sleep(5)

async def auto_restart():
    await bot.wait_until_ready()
    await asyncio.sleep(86400)
    await bot.logout()

cogs_dir = "cogs"
for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

bot.loop.create_task(playing())
bot.loop.create_task(auto_restart())
bot.run(sett.token)
