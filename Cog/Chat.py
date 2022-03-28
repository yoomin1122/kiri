import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
from discord.ext.commands import CommandNotFound, has_permissions, MissingPermissions
import pytz
import traceback
import os
import pymysql


db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoominserver1122', db='kiri', charset='utf8')
curs = db.cursor(pymysql.cursors.DictCursor)

class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def chat(self, ctx):
        await ctx.send("개발봇 Cogs/Chat.py 출력완료")

    @commands.command()
    async def 안녕(self, ctx):
        choice = random.choice(["안녕하세요! 저는 키리라고 해요!", f"안녕하세요 {ctx.message.author.mention}님"])
        await ctx.send(choice)

    @commands.command()
    async def 뭐해(self, ctx):
        choice = random.choice(["그냥 있어요!", "명령어 학습중이에요!", f"{ctx.message.author.mention}님과 함께 있어요!"])
        await ctx.send(choice)

    @commands.command()
    async def 잼민이(self, ctx):
        choice = random.choice(["저는 잼민이 안좋아해요.. 으..", "잼민이 하니깐 누군가 생각나는건 기분탓인가요? ㅎ", f"혹시 잼민이세요?"])
        await ctx.send(choice)

    @commands.command()
    async def 뭐해(self, ctx):
        choice = random.choice(["그냥 있어요!", "명령어 학습중이에요!", f"{ctx.message.author.mention}님과 함께 있어요!"])
        await ctx.send(choice)

    @commands.command()
    async def 뭐해(self, ctx):
        choice = random.choice(["그냥 있어요!", "명령어 학습중이에요!", f"{ctx.message.author.mention}님과 함께 있어요!"])
        await ctx.send(choice)

    @commands.command()
    async def 뭐해(self, ctx):
        choice = random.choice(["그냥 있어요!", "명령어 학습중이에요!", f"{ctx.message.author.mention}님과 함께 있어요!"])
        await ctx.send(choice)

    @commands.command()
    async def 뭐해(self, ctx):
        choice = random.choice(["그냥 있어요!", "명령어 학습중이에요!", f"{ctx.message.author.mention}님과 함께 있어요!"])
        await ctx.send(choice)
    @commands.command() 
    async def 회원가입(self, ctx):
        user = ctx.author
        sql = f"INSERT INTO `kiri`.`mem` (`user_id`, `user_name`, `money`) VALUES ('{user.id}', '{user.name}', '10000');"
        curs.execute(sql)
        db.commit()
        await ctx.send(f"회원가입 완료")
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('마법의 소라고동님 '):
            choice = random.choice(["그럼", "안돼", "맘대로해"])
            await message.channel.send(choice)

def setup(bot):
    bot.add_cog(Chat(bot))