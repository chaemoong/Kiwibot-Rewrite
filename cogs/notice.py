import discord
from discord.ext import commands
import asyncio
from cogs.utils import option

class notice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text = ""
        self.channels = []		
        self.success = []
        self.failed = []
        self.channel_cant_make = []

    async def get_announce_channel(self):
        for guild in self.bot.guilds:
            Allow = False
            for channel in guild.channels:
                if guild.id in [channel.guild.id for channel in self.channels]: break
                
                for Prefix in option.allowprefix:
                    if Prefix in channel.name:                        
                        Allow = True
                        
                for Prefix in option.disallowprefix:
                    if Prefix in channel.name:
                        Allows = False
                        
                if Allow and isinstance(channel, discord.TextChannel) and not channel in self.channels:
                    self.channels.append(channel)
                    break
                    
            if option.nfct and not guild.id in [channel.guild.id for channel in self.channels]:
                channel = await self.create_announce_channel(guild)
                if channel:
                    self.channels.append(channel)
        
    async def create_announce_channel(self, guild):
        try:
            return await guild.create_text_channel(option.nfctname, reason="Because of DPNK")
        except Exception as e:
            self.channel_cant_make.append((guild, e))
            return None
            
    def make_tasks(self):
        return [self.send(channel) for channel in self.channels]
            
    async def send(self, channel):
        try:
            em = discord.Embed(colour=0xfcf794)
            em.add_field(name="키위봇 공지", value=self.text + "\n\n[[ 키위봇 초대하기! ]](http://invite.kiwibot.kro.kr/)\n[[ 키위봇 공식서버! ]](https://discord.gg/wb5JgQt)")
            self.success.append(await channel.send(embed=em))
        except Exception as e:
                self.failed.append((channel, e))
            
    async def announce(self, text):
        self.text = text
        await self.get_announce_channel()
        await asyncio.wait(self.make_tasks())
        

            
    async def process_command(self, message):
        if message.content.startswith(option.command) and message.author.id in option.owner:
            notice_text = message.content[len(option.command):]
            
            embed = discord.Embed(title="DPNK - StayCute", color=0xfcf794)
            msg = await message.channel.send(message.author.mention, embed=embed)
            
            await self.get_announce_channel()
            
            embed = discord.Embed(title="DPNK - StayCute", color=0xb4fc94, description="발신중 입니다")
            await msg.edit(embed=embed)
            
            await self.announce(notice_text)
            await msg.delete()
            
            escape_drop = '\n'
            
            await message.channel.send(f"""**✅ 공지를 발신하였습니다

공지 발신 성공 채널:
`{len(self.success)}`개의 채널에 송신하였습니다.

공지 발신 실패 채널:
```
{escape_drop.join([f'{channel.name} [{type(error)}]' for channel, error in self.failed])} 
```

공지 채널 생성 실패:
```
{escape_drop.join([f'{guild.name} [{type(error)}]' for guild, error in self.channel_cant_make])} 
```**

__Sending With DPNK__""")

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.process_command(message)
    
def setup(bot):
    bot.add_cog(notice(bot))
