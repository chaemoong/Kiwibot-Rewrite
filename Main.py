import asyncio
import discord
import random
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CommandInvokeError
bot = commands.AutoShardedBot(command_prefix='k!')



@bot.event
async def on_ready():
    print('{0.user} 계정에 로그인 하였습니다!'.format(bot))
    bot.remove_command('help')
    bot.load_extension('cogs.help')
    
async def playing():
    await bot.wait_until_ready()

    status = ['도움말은 k!help으로 받을 수 있어요!', '{} SERVERS | {} USERS'.format(len(bot.guilds), len(set(bot.get_all_members()))), '키위봇은 꾸준히 성장중이에요!']

    while not bot.is_closed():
        for i in status:
            await bot.change_presence(activity=discord.Game(i))
            await asyncio.sleep(5)

for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py"):
        try:
            cog = ['owner', 'general', 'error']
            for i in cog:
                try:
                    bot.load_extension('cogs.' + i)
                except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                    pass
        except Exception as e:
            raise e

bot.loop.create_task(playing())
bot.run('NTM4NjU5NTgwODU1NDUxNjQ4.XOK0Dg.-VvsDXLr8dW-NS_hkgbX2YZgtow')
