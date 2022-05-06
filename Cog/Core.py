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
from discord_kartrider import kartrider as kart
from discord_slash.utils.manage_commands import create_option, create_choice

riot_token = ""
naver_dev_id = ""
naver_dev_pass = ""
api_key = ""

class Core(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="hellothisisverification")
    async def _test(self, ctx: SlashContext):
        await ctx.send("YooMin1122#5973 (433183785564110848)")
    @commands.command()
    async def print(self, ctx):
        await ctx.send("개발봇 Cogs/Core.py 출력완료")
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
    
    @commands.command(aliases=["도움", "commands", "도움말"])
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

    @cog_ext.cog_slash(name="번역", description="원하는 문장을 번역 해보세요!",
        options=[
            create_option(name="blanguage", description="작성할 문장의 언어를 선택 해주세요!", required=True, option_type=3,
                choices=[
                    create_choice(name="한국어",value="ko"),
                    create_choice(name="영어",value="en"),
                    create_choice(name="일본어",value="ja"),
                    create_choice(name="중국어(간체)",value="zh-CN"),
                    create_choice(name="베트남어",value="vi"),
                    create_choice(name="인도네시아어",value="id"),
                    create_choice(name="독일어",value="de"),
                    create_choice(name="러시아어",value="ru"),
                    create_choice(name="스페인어",value="es"),
                    create_choice(name="이탈리아어",value="it"),
                    create_choice(name="프랑스어",value="fr") ]),
            create_option(name="alanguage", description="문장을 번역할 언어를 선택 해주세요!", required=True, option_type=3,
                choices=[
                    create_choice(name="한국어",value="ko"),
                    create_choice(name="영어",value="en"),
                    create_choice(name="일본어",value="ja"),
                    create_choice(name="중국어(간체)",value="zh-CN"),
                    create_choice(name="베트남어",value="vi"),
                    create_choice(name="인도네시아어",value="id"),
                    create_choice(name="독일어",value="de"),
                    create_choice(name="러시아어",value="ru"),
                    create_choice(name="스페인어",value="es"),
                    create_choice(name="이탈리아어",value="it"),
                    create_choice(name="프랑스어",value="fr") ]),
            create_option(name="text", description="번역할 문장을 작성 해주세요!", required=True, option_type=3  )])

    async def _translate(self, ctx: SlashContext, blanguage: str, alanguage: str, text: str):
        add = translatetool.translate(naver_dev_id, naver_dev_pass)
        add1 = await add.translate(blanguage, alanguage, text)
        embed = discord.Embed(color=0x6758f0)
        if blanguage == alanguage:
            embed.set_author(name=f"error")
            embed.add_field(name="원문과 번역할 언어가 같습니다 다시 선택해주세요", value="ex) 번역 한국어 영어", inline=False)
        else:
            embed.set_author(name=f"파파고 {blanguage} -> {alanguage} 번역", icon_url="https://papago.naver.com/static/img/papago_og.png")
            embed.add_field(name=":arrow_down: | 원문", value=text, inline=False)
            embed.add_field(name=":white_check_mark: | 번역문", value=add1, inline=False)
            embed.set_footer(text="약간의 오역이 있을수 있습니다.")
        await ctx.send(embed=embed)

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

    @commands.command()
    async def 롤(self, ctx, *, UserName):
            UserInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + UserName
            requests = requests.get(UserInfoUrl, headers={"X-Riot-Token":riot_token})
            requests_js = json.loads(requests.text)

            if requests.status_code == 200:
                UserIconUrl = "http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/{}.png"
                embed = discord.Embed(title=f"{requests_js['name']} 님의 플레이어 정보", description=f"**{requests_js['summonerLevel']} LEVEL**", color=0x6758f0)

                UserInfoUrl_2 = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + requests_js["id"]
                res_2 = requests.get(UserInfoUrl_2, headers={"X-Riot-Token":riot_token})
                res_2js = json.loads(res_2.text)

                if res_2js == []:
                    embed.add_field(name=f"{requests_js['name']} 님은 언랭크입니다.", value="**언랭크 유저의 정보는 출력하지 않습니다.**", inline=False)
                else:
                    for rank in res_2js:
                        if rank["queueType"] == "RANKED_SOLO_5x5":
                            embed.add_field(name="솔로랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
                        else:
                            embed.add_field(name="자유랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
                embed.set_author(name=requests_js['name'], url=f"http://fow.kr/find/{UserName.replace(' ', '')}", icon_url=UserIconUrl.format(requests_js['profileIconId']))
                await ctx.send(embed=embed)

            else:
                error = discord.Embed(title="존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.", color=0xFF9900)
                await ctx.send(embed=error)

    @commands.command(aliases=['프사'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def 아바타(self, ctx, user: discord.User):
        embed = discord.Embed(color=0x6758f0, description=f"[링크]({user.avatar_url})")
        embed.set_author(name=user.name)
        embed.set_image(url=user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @아바타.error
    async def 아바타_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"쿨타임이 {round(error.retry_after)}초 남았습니다")

def setup(bot):
    bot.add_cog(Core(bot))
