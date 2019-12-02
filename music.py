"""
This is an example cog that shows how you would make use of Lavalink.py.
This example cog requires that you have python 3.6 or higher due to the f-strings.
"""
import math
import re

import discord
import lavalink
from discord.ext import commands
import datetime
import inspect
import os
import time
from pytz import timezone, utc
from discord import Spotify
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from discord import VoiceRegion
from discord import Game
import subprocess
import sys
import time
import json


url_rx = re.compile('https?:\\/\\/(?:www\\.)?.+')  # noqa: W605


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.a = 'data/music/settings.json'
        self.setting = dataIO.load_json(self.a)

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('localhost', 8080, 'youshallnotpass', 'eu', 'default-node')  # Host, Port, Password, Region, Name            
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        bot.lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)
            # Disconnect from the channel -- there's nothing else to play.

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.


    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """노래를 검색해서 노래를 틀어줘!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('노래를 찾을 수 없어요!, 다른 검색어를 입력해주세요!')

        embed = discord.Embed(color=discord.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':           
            tracks = results['tracks']
            a = await ctx.send(f'이 플레이 리스트에는 총 {len(tracks)} 개의 노래(혹은 영상)들이 담겨 있습니다!\n재생 하시려면 `재생` 안하시려면 `취소` 아니면 30초동안 기달려주세요!')
            msg = await self.bot.wait_for('message', timeout=30)
            b = int(msg.content)
            if b == '재생':
                for track in tracks:
                    player.add(requester=ctx.author.id, track=track)

                embed.title = '재생목록에 추가된 노래!'
                embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} 곡들을 추가했습니다!'
            elif b == '취소':
                await a.edit('정상적으로 취소되었습니다!')               
        else:
            track = results['tracks'][0]
            embed.title = '재생목록에 추가된 노래'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})를 재생목록에 추가했어요!'
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        if not player.is_playing:
            await ctx.send(f'`[{track["info"]["title"]}]` 노래를 재생할게요!')
            if f'{ctx.guild.id}' in self.setting:
                await player.play()
                await player.set_volume(self.setting[f'{ctx.guild.id}']['volume']) 
            else:
                await player.play()

    @commands.command()
    async def seek(self, ctx, *, seconds: int):
        """선택한 초로 건너뛰게 해주는 명령어야!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)

        await ctx.send(f'**{lavalink.utils.format_time(track_time)}**초로 넘길께요!')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int = None):
        """노래 플레이어의 볼륨을 설정하는 명령어야!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        em=discord.Embed(colour=ctx.author.colour)

        if volume is None:
            em.add_field(name='현재 볼륨', value=f'🔈 | {player.volume}%')
        try:
            if volume < 0 or volume > 150:
                return await ctx.send('볼륨은 1~150% 로 맞춰야되요!')
        except:
            pass
        else:
            try:
                self.setting[f'{ctx.author.guild.id}'].update({"volume": volume})
            except KeyError:
                self.setting[f'{ctx.author.guild.id}'] = {}
                self.setting[f'{ctx.author.guild.id}'].update({"volume": volume})
            await player.set_volume(volume)
            em.add_field(name='볼륨 설정', value=f'🔈 | {player.volume}% 으로 설정했어요!')
        await ctx.send(embed=em)
        dataIO.save_json(self.a, self.setting)

    @commands.command(aliases=['forceskip'])
    async def skip(self, ctx):
        """이 노래를 건너뛰게 하는 명령어야!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('노래를 재생하고 있지 않아요!')

        await player.skip()
        await ctx.send('⏭ | 건너 뛰어 다른 노래로 레츠기릿!')

    @commands.command(aliases=['np', 'n', 'playing'])
    async def now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.current:
            return await ctx.send('노래를 재생하고 있지 않아요! 노래를 추가해주세요!')

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 라이브 스트리밍'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=discord.Color.blurple(),
                              title='지금 재생중', description=song)
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int = 1):
        """ Shows the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('노래를 재생하고 있지 않아요!')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=discord.Color.blurple(),
                              description=f'**{len(player.queue)} 노래**\n\n{queue_list}')
        embed.set_footer(text=f'페이지 수:{page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        """노래를 일시정지 하고 해제 하는  명령어야!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('노래를 재생하고 있지 않아요!')

        if player.paused:
            await player.set_pause(False)
            await ctx.send('⏯ | 다시 음악좀 올릴게유!')
        else:
            await player.set_pause(True)
            await ctx.send('⏯ | 잠시 음악좀 멈출게유!')

    @commands.command()
    async def shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('노래를 재생하고 있지 않아요!')

        player.shuffle = not player.shuffle
        await ctx.send('🔀 | 재생목록 랜덤으로 ' + ('하기!' if player.shuffle else '안하기!'))

    @commands.command(aliases=['loop'])
    async def repeat(self, ctx):
        """ Repeats the current song until the command is invoked again. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('노래를 재생하고 있지 않아요!')

        player.repeat = not player.repeat
        await ctx.send('🔁 | 반복모드 ' + ('켜기!' if player.repeat else '끄기!'))

    @commands.command()
    async def remove(self, ctx, index: int):
        """ Removes an item from the player's queue with the given index. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('노래를 재생하고 있지 않아요!')

        if index > len(player.queue) or index < 1:
            return await ctx.send(f'**무조건** 1 아니면 {len(player.queue)} 보다 커야되!')

        removed = player.queue.pop(index - 1)  # Account for 0-index.

        await ctx.send(f'**{removed.title}**곡이 재생목록에서 지웠어!')

    @commands.command()
    async def search(self, ctx, *, query):
        """곡을 검색하는 명령어 입니다!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query
        
        if query.startswith('scsearch: '):
            query = 'scsearch: ' + query

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('곡이 검색해서 찾을수 없어! 미안하지만 다른 곡으로 해주겠어?')

        tracks = results['tracks'][:10]  # First 10 results

        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'

        embed = discord.Embed(color=discord.Color.blurple(), description=o)
        await ctx.send(embed=embed)

    @commands.command()
    async def stop(self, ctx):
        """재생목록을 비우고 연결을 끊습니다!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('봇이 음악을 켜지 않았습니다!')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('같은 보이스 채널에 있어야 이 명령어를 쓸수 있어욧!')

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | 재생목록을 초기화 하고 보이스채널에서 나왔어!')

    @commands.command()
    async def stop_disconnecting(self, ctx):
        """봇이 강제로 끊겼을때, 재접속할수 있게 됩니다!"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | 재생목록을 초기화 완료!!')


    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.players.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.

        should_connect = ctx.command.name in ('play')

        if should_connect:
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))

        if not player.is_connected:
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                return await ctx.send('봇에 권한이 없어요 ㅜㅜ, 봇에게 관리자 권한을 추가해주세요!')

            player.store('channel', ctx.channel.id)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                return await ctx.send('당신은 저랑 같은 보이스 채널이 있지 않아요!')


def setup(bot):
    bot.add_cog(Music(bot))