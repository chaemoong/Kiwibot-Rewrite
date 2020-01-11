import discord
from discord.ext import commands
import traceback
import json
from discord.utils import get
from cogs.utils.dataIO import dataIO
import asyncio
import random
import os
import datetime
import time

class Blacklisted(commands.CheckFailure): pass

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setting = 'data/mod/settings.json'
        self.ko = 'data/language/ko.json'
        self.en = 'data/language/en.json'
        self.welcome = 'data/mod/welcome.json'

    def __global_check_once(self, ctx):
        blacklist = dataIO.load_json('blacklist.json')
        if str(ctx.author.id) in blacklist:
            raise Blacklisted()
        else:
            return True
   
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        asdf = dataIO.load_json(self.setting)
        try:
            if asdf[f'{ctx.guild.id}']['language'] == 'ko':
                data = dataIO.load_json(self.ko)
            else:
                data = dataIO.load_json(self.en)
        except:
            data = dataIO.load_json(self.en)
        if isinstance(error, commands.CommandInvokeError):
            # A bit hacky, couldn't find a better way
            no_dms = "Cannot send messages to this user"
            is_help_cmd = ctx.command.qualified_name == "help"
            is_forbidden = isinstance(error.original, discord.Forbidden)
            if is_help_cmd and is_forbidden and error.original.text == no_dms:
                msg = ("당신에게 DM으로 보내드리려고 했는데 전송이 안되요! DM차단을 풀어주시면 다시 시도 하시면 보내드리겠어요!\nI was going to send it to you by DM, but it's not! If you untie the DM block, I'll send it to you!")
                await ctx.send(msg)
                return
            em = discord.Embed(title='에러! | ERROR!', colour=discord.Colour.red())
            em.add_field(name='에러 발생한 명령어 | Error generated command', value=ctx.command.qualified_name)
            em.set_footer(text=f'에러가 지속적으로 발생할시 {self.bot.get_user(431085681847042048)}으로 문의 바랍니다!\nIf that command Error generated again contact {self.bot.get_user(431085681847042048)} ({self.bot.get_user(431085681847042048).id})')
            log = ("Exception in command '{}'\n"
                   "".format(ctx.command.qualified_name))
            log += "".join(traceback.format_exception(type(error), error,
                                                      error.__traceback__))
            print(log)
            await ctx.send(embed=em)
        elif isinstance(error, commands.CommandNotFound):
            lan = data['command_none']
            em = discord.Embed(colour=ctx.author.colour)
            em.add_field(name=lan['1'], value=lan['2'].format(ctx))
            em.set_footer(text=lan['3'])
            return await ctx.send(embed=em)
        elif isinstance(error, commands.CheckFailure):
            lan = data['admin_command']
            em = discord.Embed(colour=ctx.author.colour)
            em.add_field(name=lan['1'], value=lan['2'].format(ctx))
            em.set_footer(text=lan['3'])
            return await ctx.send(embed=em)
        elif isinstance(error, commands.CommandOnCooldown):
            asdf = time.strftime("%M", time.gmtime(error.retry_after))
            asss = time.strftime("%S", time.gmtime(error.retry_after))
            em = discord.Embed(colour=ctx.author.colour)
            em.add_field(name='쿨타임 발생!', value=f'이 명령어 에는 쿨타임이 걸려있습니다!\n`{asdf}분 {asss}초` 후에 다시 시도 해주세요!')
            return await ctx.send(ctx.author.mention, embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == True:
            return
        if message.guild == None:
            a = 'Direct Message'
        else:
            a = f"{message.guild}({message.guild.id})"
        print(f'Server: {a}, Author: {message.author}({message.author.id}), Content: {message.content}')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = dataIO.load_json(self.welcome)
        a = data.get(str(member.guild.id))
        if a == None:
            return
        if a.get('message1') == None:     
            await self.bot.get_channel(a.get('channel')).send(f'{member.mention}님! {member.guild}서버에 오신것을 환영합니다!')
        else:
            await self.bot.get_channel(a.get('channel')).send(a.get('message1'))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        data = dataIO.load_json(self.welcome)
        a = data.get(str(member.guild.id))
        if a == None:
            return
        if a.get('message2') == None:     
            await self.bot.get_channel(a.get('channel')).send(f'{member}님아 {member.guild}서버에서 나가셨습니다')
        else:
            await self.bot.get_channel(a.get('channel')).send(a.get('message2'))

def check_folder():
    if not os.path.exists('data/language'):
        print('data/language 풀더생성을 완료하였습니다!')
        os.makedirs('data/language')

def check_file():   
    data = {
        "userinfo": {
            "1": "Offline",
            "2": "Web :globe_with_meridians:",
            "3": "Mobile :iphone:",
            "4": "Desktop :desktop:",
            "game": "Playing {}",
            "Spotify": "Listening to `{}` of `{}` in Spotify",
            "5": "Nope",
            "6": "USERINFO",
            "7": "USER TAG",
            "9": "Activity",
            "10": "Resitered Date",
            "12": "Client",
            "13": "Joined Date",
            "14": "Roles",
            "15": "It's over the role, so i can't print any more!",
            "time": "%Y-%m-%d %H:%M (UTC)"
        },
        "command_none": {
            "1": "The command is not a command!",
            "2": "Check the command with `{0.prefix}help`!",
            "3": "Please check that you wrote it correctly and use it!"
        },    
        "admin_command": {
            "1": "The command is only Administrator command!",
            "2": "Check the command with `{0.prefix}help` to you can use command!",
            "3": "Don't use Administrator without Administrator permission!"
        },
        "serverinfo": {
            "time": "%Y-%m-%d %H:%M (UTC)",
            "1": "None",
            "2": "Serverinfo",
            "3": "Server Name",
            "4": "Server ID",
            "5": "Region",
            "6": "Created at",
            "7": "Server Owner",
            "8": "It's over the role, so i can't print any more!",
            "9": "roles",
            "10": "Member Count (include bot)",
            "11": "**{} persons**",
            "none" : "**None (Unrestricted!)**",
            "low": "**Low (Must have a verified email on their Diacord account!)**",
            "medium":"**Medium (Must also be registered on Discord for longer than 5 minutes!)**",
            "high": "**(╯°□°）╯︵ ┻━┻(high) (Must also be a member of  this server for longer than 10 minutes)**",
            "extreme": "**┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻(extreme) (Must have a verified phone on their Discord account!)**"
        },
        "chinobot": {
            "1": "Chinobot's PING",
            "2": "Chinobot's Member Count",
            "3": " persons",
            "4": "Chinobot's Server count",
            "6": "Chinobot's Uptime",
            "5": " servers"
        },
        "ban": {
            "1": "> Mention user to Ban",
            "2": "None",
            "3": "> The user banned!\nReason: {}",
            "4": "> Either I don't have permission or have a problem with the Discord API.\nPlease add more rights and try again. If not, please try again later because it is API problem."
        },
        "unban": {
            "1": "> Wrote user ID to unban",
            "2": "None",
            "3": "> The user unbanned!\nReason: {}",
            "4": "> Either I don't have permission or have a problem with the Discord API.\nPlease add more rights and try again. If not, please try again later because it is API problem.",
            "5": "> I can't find the User",
            "6": "This user is not banned"

        },
        "hackban": {
            "1": "> Wrote user ID to hackban",
            "2": "None",
            "3": "> The user hackbanned!\nReason: {}",
            "4": "> Either I don't have permission or have a problem with the Discord API.\nPlease add more rights and try again. If not, please try again later because it is API problem.",
            "5": "Already This user is banned"
        },
        "kick": {
            "1": "> Mention user to Kick",
            "2": "None",
            "3": "> The user Kicked!\nReason: {}",
            "4": "> Either I don't have permission or have a problem with the Discord API.\nPlease add more rights and try again. If not, please try again later because it is API problem."
        },
        "경고": {
            "1": "You were banned on server {}",
            "2": "Reason: Ban due to over the warnings",
            "3": "If you have any complaints, please contact {author}({author.id})",
            "4": "Occurred Warnings!",
            "5": "{} ({}) was ban due to over-warnings",
            "6": "{} received one warning!\n If the user has {} warnings, the user will be Ban!\n reason: {}\n Current number of warnings: {}",
            "7": "> Please mention users give a warning",
            "8": "> Warn command not available for bot!",
            "9": "None",
            "10": "Ban due to over the warnings",
            "me": "> You can't warn yourself!"
        },
        "unwarn": {
            "1": "> Mention the user to clear a warning!",
            "2": "> Warn command not available for bot!",
            "3": "None",
            "4": "> No warning data for that user!",
            "5": "Success!",
            "6": "I've removed a warning from the user!"
        },
        "check": {
            "2": "> Warn command not available for bot!",
            "3": "Warning Count",
            "5": "{} has 0 warnings",
            "6": "{} has {} warnings and the reasons are as follows!",
            "7": "Reason"
        },
        "clean": {
            "1": "> Mention the user to clear a warning!",
            "2": "> Warn command not available for bot!",
            "3": "None",
            "4": "> No warning data for that user!",
            "5": "Success!",
            "6": "{}'s warnings has been initialized to 0!"
        },
        "limit":{
            "1": "> The number of warning limits should be more than 1 or so!!",
            "2": "You have to write down the warning limits!",
            "5": "Success!",
            "6": "Warn limit set to {}!"
        },
        "modset": {
            "admin": {
                "1": "> Mention the role to setting a adminstrator role!",
                "2": "Success!",
                "3": "Role {} has been chosen as administrator role!"
            },
            "mod": {
                "1": "> Mention the role to setting a moderator role!",
                "2": "Success!",
                "3": "Role {} has been chosen as moderator role!"
            },
            "log": {
                "1": "> Mention the channel to setting a log channel!",
                "2": "Success!",
                "3": "Channel {} has been chosen as log channel!"
            },
            "filter": {
                "1": "on",
                "2": "off",
                "3": "Success!",
                "4": "The bad words filter is now Turn {}!"
            },
            "role": {
                "1": "> Mention the role to setting a captcha role!",
                "2": "Success!",
                "3": "Role {} has been chosen as captcha role!"
            },
            "channel": {
                "1": "> Mention the channel to setting a captcha channel!",
                "2": "Success!",
                "3": "Channel {} has been chosen as captcha channel!"
            }
        },
        "log": {
            "1": "None",
            "2": "%Y-%m-%d %H:%M (UTC)",
            "3": "Time of occurrence: {}",
            "4": "USER(ID) | Administrator(ID)",
            "5": "Reason",
            "6": "Warning Count"
        },
        "afk": {
            "1": "잠수 시작! | AFK START!",
            "2": "{}'s afk started!",
            "3": "Please fill out any message to terminate the afk!",
            "4": "Reason"
        },
        "end": {
            "1": "{} has finished afk!\n\nReason: {}\n\nWhere have you been!?",
            "2": "{} has finished afk!\n\nWhere have you been?",
            "3": "잠수 끝! | AFK END!"
        },
        "verify": {
            "1": "> No CAPTCHA {} is set! Ask the administrator!",
            "channel": "channel",
            "role": "role",
            "2": "> Please use the authentication command on the authentication channel!",
            "3": "> You've already been verified!",
            "4": "{} error has occurred! Error content: {}",
            "5": "Please watch the DM!",
            "6": "Welcome to {}!",
            "7": "This feature is designed to protect the server and prevent the self-bot from becoming a Captcha function!\nPlease write down the code on the image.!",
            "8": "> Cancel the Captcha!",
            "9": "> Complete!",
            "10": "The CAPTCHA key is invalid! Please try again!"
        }
    }
    data2 = {
        "userinfo": {
            "1": "오프라인",
            "2": "웹 :globe_with_meridians:",
            "3": "모바일 :iphone:",
            "4": "데스크톱 :desktop:",
            "game": "{} 플레이중",
            "Spotify": "Spotify 에서 `{}`의 `{}` 노래 듣는중",
            "5": "없음",
            "6": "유저정보",
            "7": "유저 태그",
            "9": "활동",
            "10": "계정 생성일",
            "12": "디스코드 클라이언트",
            "13": "서버 가입일",
            "14": "역할",
            "15": "역할이 너무 많이 출력 할 수 없습니다!",
            "time": "%Y년 %m월 %d일 %H시 %M분 (UTC)"
        },    
        "command_none": {
            "1": "그 명령어는 없는 명령어 입니다!",
            "2": "`{0.prefix}help` 으로 명령어를 확인하세요!",
            "3": "제대로 작성하였는지 확인해주시고 사용해주세요!"
        },    
        "admin_command": {
            "1": "그 명령어는 관리자 명령어 입니다!",
            "2": "`{0.prefix}help` 으로 사용할수 있는 명령어를 확인하세요!",
            "3": "관리자 권한 없이 관리자 명령어를 사용하지 마세요!"
        },
        "serverinfo": {
            "time": "%Y년 %m월 %d일 %H시 %M분 (UTC)",
            "1": "없음",
            "2": "서버 정보",
            "3": "서버 이름",
            "4": "서버의 ID",
            "5": "서버 위치",
            "6": "서버 생성일",
            "7": "서버 주인",
            "8": "역할이 너무 많이 출력 할 수 없습니다!",
            "9": "역할",
            "none" : "**없음 (아무 제한도 없어요!)**",
            "low": "**낮음 (자신의 디스코드 계정이 이메일 인증을 받은적이 있어야 해요!)**",
            "medium":"**중간 (자신의 디스코드 계정이 이메일 인증을 받은적이 있어야 하고 가입한지 5분이 지나야 합니다!)**",
            "high": "**높음 (자신의 디스코드 계정이 이메일 인증을 받은적이 있어야 하고 가입한지 5분이 지나야 하고 멤버가 된지 10분이 되어야 합니다!)**",
            "extreme": "**매우 높음 (전화 인증이 완료된 디스코드 계정 이여야 합니다!)**"   
        },
        "chinobot": {
            "1": "치노봇 핑",
            "2": "치노봇 유저수",
            "3": " 명",
            "4": "치노봇 서버수",
            "6": "치노봇 업타임 시간",
            "5": " 개"
        },
        "ban": {
            "1": "> 벤할 유저를 멘션해주세요",
            "2": "없음",
            "3": "> 벤이 정상적으로 진행되었어요!\n 사유: {}",
            "4": "> 권한이 없거나 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주신 후 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!"
        },
        "kick": {
            "1": "> 킥할 유저를 멘션해주세요",
            "2": "없음",
            "3": "> 킥이 정상적으로 진행되었어요!\n 사유: {}",
            "4": "> 권한이 없거나 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주신 후 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!"
        },
        "unban": {
            "1": "> 언벤할 유저의 ID를 보내주세요!",
            "2": "없음",
            "3": "> 이 유저는 언벤 되었습니다!\n사유: {}",
            "4": "> 권한이 없거나 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주신 후 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!",
            "5": "> 그 유저를 찾을 수 없습니다",
            "6": "이 유저는 벤이 되어있지 않습니다!"

        },
        "hackban": {
            "1": "> 핵벤할 유저의 ID를 보내주세요!",
            "2": "없음",
            "3": "> 이 유저는 핵벤 되었습니다!\n사유: {}",
            "4": "> 권한이 없거나 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주신 후 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!",
            "5": "이 유저는 이미 벤 되어있습니다!"
        },
        "경고": {
            "1": "당신은 {} 서버에서 벤 당하셨습니다!",
            "2": "사유: 경고 초과로 인한 벤",
            "3": "해당 사항에 문의하실게 있으시다면 {}({}) 님에게 문의해주세요",
            "4": "경고 발생!",
            "5": "{} 님은 경고 초과로 인하여 벤 되었습니다!",
            "6": "{} 님은 경고 1회를 받으셨습니다!\n만약 그 유저의 경고가 {} 개가 될경우 그 유저는 벤이 됩니다!\n사유: {}\n현재 경고 개수: {}",
            "7": "> 경고를 줄 유저를 멘션해주세요!",
            "8": "> 봇에게 경고 명령어를 사용할 수 없습니다!",
            "9": "없음",
            "10": "경고 초과로 인한 벤",
            "me": "> 자기 자신에게 경고를 줄수 없습니다!"
        },
        "unwarn": {
            "1": "> 경고를 지울 유저를 멘션해주세요!",
            "2": "> 봇에게 경고 명령어를 사용할 수 없습니다!",
            "3": "없음",
            "4": "> 그 유저에 대한 경고데이터가 없습니다!",
            "5": "성공!",
            "6": "그 유저의 경고를 1개 지웠습니다!"
        },
        "check": {
            "2": "> 봇에게 경고 명령어를 사용할 수 없습니다!",
            "3": "경고 수",
            "4": "> 그 유저에 대한 경고데이터가 없습니다!",
            "5": "{} 님의 경고는 0개입니다!",
            "6": "{} 님의 경고는 {}개 이며 사유는 아래와 같습니다!",
            "7": "사유"
        },
        "clean": {
            "1": "> 경고를 지울 유저를 멘션해주세요!",
            "2": "> 봇에게 경고 명령어를 사용할 수 없습니다!",
            "3": "없음",
            "4": "> 그 유저에 대한 경고데이터가 없습니다!",
            "5": "성공!",
            "6": "{} 님의 경고는 0개로 초기화 되었습니다!"
        },
        "limit":{
            "1": "> 경고 제한 갯수는 1 이상 혹은 정수 여야 되요!",
            "2": "> 경고 제한 갯수를 적어주셔야 되요!",
            "5": "성공!",
            "6": "경고 제한을 {} 으로 설정했어요"
        },
        "modset": {
            "admin": {
                "1": "`관리자 역할`로 설정할 역할을 멘션해주셔야 됩니다!",
                "2": "성공!",
                "3": "{} 역할을 관리자 역할로 정했습니다!"
            },
            "mod": {
                "1": "`부관리자 역할`로 설정할 역할을 멘션해주셔야 됩니다!",
                "2": "성공!",
                "3": "{} 역할을 부관리자 역할로 정했습니다!"
            },
            "log": {
                "1": "`처벌 로그`로 설정할 채널을 멘션해주셔야 됩니다!",
                "2": "성공!",
                "3": "{} 채널을 처벌 로그 채널로 정했습니다!"
            },
            "filter": {
                "1": "켜",
                "2": "꺼",
                "3": "성공",
                "4": "욕필터는 이제 {}졌습니다!"
            },
            "role": {
                "1": "`인증(캡챠) 역할`로 설정할 역할을 멘션해주셔야 됩니다!",
                "2": "성공!",
                "3": "{} 역할을 인증(캡챠) 역할로 정했습니다!"
            },
            "channel": {
                "1": "`인증(캡챠) 로그`로 설정할 채널을 멘션해주셔야 됩니다!",
                "2": "성공!",
                "3": "{} 채널을 인증(캡챠) 채널로 정했습니다!"
            }

        },
        "log": {
            "1": "없음",
            "2": "%Y년 %m월 %d일 %H시 %M분 (UTC)",
            "3": "발생 시간: {}",
            "4": "유저 (ID) | 관리자 (ID)",
            "5": "사유",
            "6": "경고 개수"
        },
        "afk": {
            "1": "잠수 시작! | AFK START!",
            "2": "{} 님의 잠수 상태가 시작되었습니다!",
            "3": "잠수 상태를 해지 하시려면 아무 메시지나 작성해주세요!",
            "4": "사유"
        },
        "end": {
            "1": "{} 님의 잠수 상태가 끝났습니다!\n.\n사유: {}\n.\n어디 다녀 오셨나요!?",
            "2": "{} 님의 잠수 상태가 끝났습니다!\n\n어디 다녀 오셨나요!?",
            "3": "잠수 끝! | AFK END!"
        },
        "verify": {
            "1": "> 설정된 캡챠(인증) {}이 없습니다! 관리자 에게 문의해보세요!",
            "channel": "채널",
            "role": "역할",
            "2": "> 인증 명령어는 인증 채널에서 사용해주세요!",
            "3": "> 이미 인증되셨습니다!",
            "4": "{} 오류가 발생했습니다! 오류 내용: {}",
            "5": "DM을 봐주세요!",
            "6": "{} 서버에 오신것을 환영합니다!",
            "7": "이 기능은 서버의 보안을 위함, 셀프봇 방지로 인하여 캡챠 기능이 생겼습니다!\n이미지에 적힌 코드를 적어주세요!",
            "8": "> 캡차가 취소 되었습니다!",
            "9": "> 완료 되었습니다!",
            "10": "> 캡챠키가 올바르지 않습니다! 다시 시도 해주세요!"
        }
    }
    blacklist = {'blacklist': []}
    f = "data/language/en.json"
    fg = "data/language/ko.json"
    thinking = 'blacklist.json'
    if not dataIO.is_valid_json(f):
        print("data/mod/settings.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)
    if not dataIO.is_valid_json(fg):
        print("error.json 파일생성을 완료하였습니다!")
        dataIO.save_json(fg,
                         data2)
    if not dataIO.is_valid_json(thinking):
        print("error.json 파일생성을 완료하였습니다!")
        dataIO.save_json(thinking,
                         blacklist)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(error(bot))
