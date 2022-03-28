from asyncio.events import BaseDefaultEventLoopPolicy
import os
from pydoc import describe
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import random
import time
import datetime
import sys
import re
import translatetool
import urllib.request
import json
import asyncio
from googleapiclient.discovery import build
from discord.utils import get
import requests
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import  create_actionrow, create_button
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import ButtonStyle
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from discord_slash.model import SlashCommandOptionType
from pp import *


naver_dev_id = "njGmvJeVcCGUmkeiGlVh"
naver_dev_pass = "CFVT5ESYhM"
api_key = "AIzaSyAd6nM1fRbRXT2qTSd02nvyvySRAqMovwI"

class Core(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="hellothisisverification")
    async def _test(self, ctx: SlashContext):
        await ctx.send("YooMin1122#5973 (433183785564110848)")
    @commands.command()
    async def print(self, ctx):
        await ctx.send("개발봇 Cogs/Core.py 출력완료")
    @commands.command()
    async def 급식(self, ctx):
        to_tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)    #오늘 날짜에 하루를 더함
        local_date2 = to_tomorrow.strftime("%Y.%m.%d")    #위에서 구한 날짜를 년.월.일 형식으로 저장
        local_weekday2 = to_tomorrow.weekday()    #위에서  구한 날짜의 요일값을 저장
 
        l_diet = get_diet(2, local_date2, local_weekday2)    #점심식단을 파싱해옴
        d_diet = get_diet(3, local_date2, local_weekday2)    #석식식단을 파싱해옴
 
        if len(l_diet) == 1:    #점심식단의 길이가 1일경우 = parser.py에서 식단이 없을경우 공백한자리를 반환함.
            await ctx.send("급식이 없습니다.")    #급식이 없다고 메세지 보냄
        elif len(d_diet) == 1:    #점심식단의 길이가 1이 아니고 석식식단의 길이가 1일경우 = 점심식단만 있을경우
            lunch = local_date2 + " 중식\n" + l_diet    #날짜와 "중식"을 앞에 붙여서
            await ctx.send(lunch)    #메세지 보냄
        else:    #둘다 길이가 1이 아닐경우 = 점심, 석식 식단 모두 있을 경우
            lunch = local_date2 + " 중식\n" + l_diet    #앞에 부가적인 내용을 붙여서
            dinner = local_date2 + " 석식\n" + d_diet
            await ctx.send(lunch)    #메세지를 보냄
            await ctx.send(dinner)

    @commands.command(aliases=['개발자'])
    async def hellothisisverification(self, ctx):
        await ctx.send("YooMin1122#5973 (433183785564110848)")
    @commands.command()
    async def 알람(self, ctx, c:str=None):
        if c is None:
            await ctx.send("뒤에 분을 붙여주세요! \n1분, 3분, 5분, 10분, 30분\nex)`키리야 알람 10분`")
        elif c == "1분" or c == "1" or c == "1min":
            await ctx.send(f"1분후에 알람이 울립니다!")
            await asyncio.sleep(60)
            await ctx.send(f"{ctx.message.author.mention}님 1분이 지났습니다!")
        elif c == "3분" or c == "3" or c == "3min":
            await ctx.send(f"3분후에 알람이 울립니다!")
            await asyncio.sleep(180)
            await ctx.send(f"{ctx.message.author.mention}님 3분이 지났습니다!")
        elif c == "5분" or c == "5" or c == "5min":
            await ctx.send(f"5분후에 알람이 울립니다!")
            await asyncio.sleep(300)
            await ctx.send(f"{ctx.message.author.mention}님 5분이 지났습니다!")
        elif c == "10분" or c == "10" or c == "10min":
            await ctx.send(f"10분후에 알람이 울립니다!")
            await asyncio.sleep(600)
            await ctx.send(f"{ctx.message.author.mention}님 10분이 지났습니다!")
        elif c == "30분" or c == "30" or c == "30min":
            await ctx.send(f"30분후에 알람이 울립니다!")
            await asyncio.sleep(1800)
            await ctx.send(f"{ctx.message.author.mention}님 30분이 지났습니다!")
        else: return await ctx.reply(f"{c}( 분)은 없습니다! \n1분, 3분, 5분, 10분, 30분 단위로 있으니 확인 부탁드려요")

    @commands.command(aliases=['ping'])
    async def 핑(self, ctx):
        await ctx.send(embed=discord.Embed(title=f':ping_pong: 퐁! {round(round(self.bot.latency, 4) * 1000)}ms', color=0x6758f0))  
    
    @commands.command(aliases=["help", "도움", "commands", "도움말"])
    async def 명령어(self, ctx, c:str=None):
        if c is None:
            embed = discord.Embed(color=0xfa4f4f)
            embed.set_author(name="명령어", icon_url="https://i.ibb.co/wpJj64Y/image.png")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name=":point_right: | 접두사", value="> 접두사 : `kiri ` `ki ` `키리야 ` `키리 `등이 있습니다", inline=False)
            embed.add_field(name=":loudspeaker: | 서버관리", value="> 킥, 밴, 언밴, 청소", inline=False)
            embed.add_field(name=":books:  | 번역", value=f"> 한영, 영한, 한일, 일한", inline=False)
            embed.add_field(name=":page_with_curl: | 일반", value=f"> 마법의 소라고동님 , 알람, 찬반, 단축링크, 여러 채팅들", inline=False)
            embed.add_field(name=":mag_right: | 검색", value=f"> 유튜브, 이미지, 아바타", inline=False)
            embed.add_field(name=":musical_note: | 음악", value=f"> 재생, 나가, 스킵, 반복, 볼륨(현재 개발중)", inline=False)
            embed.add_field(name=":desktop: | 키리 공식 사이트", value="> [바로가기](http://kiribot.kro.kr)", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['찬반투표'])
    async def 찬반(self, ctx, *, text):
        embed = discord.Embed(color=0xfa4f4f)
        embed.set_author(name="찬반투표")
        embed.add_field(name="투표 설명", value=text, inline=False)
        embed.add_field(name="찬성이라면", value=":thumbsup:를 눌러주세요")
        embed.add_field(name="반대라면", value=f":thumbsdown:를 눌러주세요")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    @commands.command()
    async def 한영(self, ctx, *, text):
        add = translatetool.translate(f"{naver_dev_id}", f"{naver_dev_pass}")
        # 언어: ko, en, ja, zh-CN, zh-TW, vi, id, th, de, ru, es, it, fr
        add1 = await add.translate("ko", "en", f"{text}")
        embed = discord.Embed(color=0x6758f0)
        embed.set_author(name="파파고 한국어 -> 영어 번역", icon_url="https://papago.naver.com/static/img/papago_og.png")
        embed.add_field(name=":flag_kr: | 한국어", value=text, inline=False)
        embed.add_field(name=":flag_us: | 영어", value=add1, inline=False)
        embed.set_footer(text="약간의 오역이 있을수 있습니다.", icon_url="")
        await ctx.reply(embed=embed, mention_author=False)
    @commands.command()
    async def 영한(self, ctx, *, text):
        add = translatetool.translate(f"{naver_dev_id}", f"{naver_dev_pass}")
        add1 = await add.translate("en", "ko", f"{text}")
        embed = discord.Embed(color=0xfa4f4f)
        embed.set_author(name="파파고 영어 -> 한국어 번역", icon_url="https://papago.naver.com/static/img/papago_og.png")
        embed.add_field(name=":flag_us: | 영어", value=text, inline=False)
        embed.add_field(name=":flag_kr: | 한국어", value=add1, inline=False)
        embed.set_footer(text="약간의 오역이 있을수 있습니다.", icon_url="")
        await ctx.reply(embed=embed, mention_author=False)
    @commands.command()
    async def 한일(self, ctx, *, text):
        add = translatetool.translate(f"{naver_dev_id}", f"{naver_dev_pass}")
        add1 = await add.translate("ko", "ja", f"{text}")
        embed = discord.Embed(color=0x6758f0)
        embed.set_author(name="파파고 한국어 -> 일본어 번역", icon_url="https://papago.naver.com/static/img/papago_og.png")
        embed.add_field(name=":flag_kr: | 한국어", value=text, inline=False)
        embed.add_field(name=":flag_jp: | 일본어", value=add1, inline=False)
        embed.set_footer(text="약간의 오역이 있을수 있습니다.", icon_url="")
        await ctx.reply(embed=embed, mention_author=False)
    @commands.command()
    async def 일한(self, ctx, *, text):
        add = translatetool.translate(f"{naver_dev_id}", f"{naver_dev_pass}")
        add1 = await add.translate("ja", "ko", f"{text}")
        embed = discord.Embed(color=0xfa4f4f)
        embed.set_author(name="파파고 일본어 -> 한국어 번역", icon_url="https://papago.naver.com/static/img/papago_og.png")
        embed.add_field(name=":flag_jp: | 일본어", value=text, inline=False)
        embed.add_field(name=":flag_kr: | 한국어", value=add1, inline=False)
        embed.set_footer(text="약간의 오역이 있을수 있습니다.", icon_url="")
        await ctx.reply(embed=embed, mention_author=False)
    @commands.command()
    async def 영일(self, ctx, *, text):
        add = translatetool.translate(f"{naver_dev_id}", f"{naver_dev_pass}")
        add1 = await add.translate("en", "ja", f"{text}")
        embed = discord.Embed(color=0x6758f0)
        embed.set_author(name="파파고 영어 -> 일본어 번역", icon_url="https://papago.naver.com/static/img/papago_og.png")
        embed.add_field(name=":flag_us: | 영어", value=text, inline=False)
        embed.add_field(name=":flag_jp: | 일본어", value=add1, inline=False)
        embed.set_footer(text="약간의 오역이 있을수 있습니다.", icon_url="")
        await ctx.reply(embed=embed, mention_author=False)
    @commands.command()
    async def 일영(self, ctx, *, text):
        add = translatetool.translate(f"{naver_dev_id}", f"{naver_dev_pass}")
        add1 = await add.translate("ja", "en", f"{text}")
        embed = discord.Embed(color=0xfa4f4f)
        embed.set_author(name="파파고 일본어 -> 영어 번역", icon_url="https://papago.naver.com/static/img/papago_og.png")
        embed.add_field(name=":flag_jp: | 일본어", value=text, inline=False)
        embed.add_field(name=":flag_us: | 영어", value=add1, inline=False)
        embed.set_footer(text="약간의 오역이 있을수 있습니다.", icon_url="")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def 코로나(self, ctx):
      korea = "https://api.corona-19.kr/korea/beta/?serviceKey=" # 국내 코로나 발생 동향
      apikey = "wPO1D7zh6oZqVEkC2fFc9NjlgRHUbeJyu"

      response = requests.get(korea + apikey)
      message = response.text
      data = json.loads(message)


      status = response.status_code

      if status == 200: #국내 코로나 발생동향이 정상적으로 불러와졌을경우(http200)
        embed = discord.Embed(color=0x6758f0)
        embed.set_author(name="국내 코로나 19 현황")
        embed.add_field(name="누적 확진자", value = format(data["korea"]["totalCnt"], ',')+"명")
        embed.add_field(name="일일 확진자", value = format(data["korea"]["incDec"], ',')+"명")
        embed.add_field(name="해외 유입", value = format(data["korea"]["incDecF"], ',')+"명")
        embed.add_field(name="완치자", value = format(data["korea"]["recCnt"], ',')+"명")
        embed.add_field(name="사망자", value = format(data["korea"]["deathCnt"], ',')+"명")
        embed.set_footer(text="["+format(data["API"]["updateTime"])+"]")
        await ctx.send(embed=embed)
      else:
        await ctx.send("error 다시 시도 해주세요")

    @commands.command(aliases=['shortlink'])
    async def 단축링크(self, ctx, text):
            client_id = f"{naver_dev_id}"
            client_secret = f"{naver_dev_pass}" 
            encText = urllib.parse.quote(f"{text}")
            data = "url=" + encText
            url = "https://openapi.naver.com/v1/util/shorturl"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                response = response_body.decode('utf-8')
                responseJson = json.loads(response)
                embed = discord.Embed(color=0x6758f0)
                embed.set_author(name="네이버 단축링크")
                embed.add_field(name=":bookmark: | 원본 링크", value=text, inline=False)
                embed.add_field(name=":link: | 단축된 링크", value=responseJson.get("result").get("url"), inline=False)
                embed.set_footer(text="단축링크 아시는 구나", icon_url="")
                await ctx.reply(embed=embed)
            else:
                print("Error Code:" + rescode)

    @commands.command(aliases=["img", "사진", "photo"])
    async def 이미지(self, ctx, *, search):
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=api_key).cse()
        result = resource.list(q=f"{search}", cx="231a68bfb62e8c0f8", searchType="image").execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"`{search}`을(를) 검색했을때 결과입니다.", color = 0xfa4f4f)
        embed1.set_image(url=url)
        await ctx.reply(embed=embed1, mention_author=False)
# 0xfa4f4f, 0x00FF7
def setup(bot):
    bot.add_cog(Core(bot))
