"""
Github GNU General Public License version 3.0 (GPLv3)
Copyright 매리 2018-2019, All Rights Reserved

However, this file is out of the copyright
"""

#공지할 사람의 디스코드 ID 입력
owner = [431085681847042048]
#봇의 토큰 입력
token = "NTM4NjU5NTgwODU1NDUxNjQ4.XgtjlA.K4cufv3qWHWL87gGlUytP6kDXJw"
#봇의 접두사 입력
first = ".."
#봇의 공지 명령어 입력
no = "공지"

command = first + no

#공지 채널을 찾을 수 없을 시
nfct = False # ( True : 채널 생성후 발송, False : 아무것도 안함 )
#생성할 채널 이름
nfctname = "공지"

""" 공지 채널 설정입니다. (자신없으면 기본으로) 반드시 List 형이여야 합니다. """

#허용 공지 채널 접두사
allowprefix = ["notice", "공지"]

#허용 공지 채널 접두사가 들어있다 하더라도 이 접두사가 들어가 있으면 공지 하지 않습니다.
disallowprefix = ["밴", "경고", "제재", "길드", "ban", "worry", "warn", "guild"]
