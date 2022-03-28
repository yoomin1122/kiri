import os

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import random
import time
import datetime
import traceback
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import aiohttp
import urllib 

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def user(self, ctx):
        await ctx.send("개발봇 Cogs/player.py 출력완료")

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

    @commands.command()
    async def opgg(self, ctx):
        soup = BeautifulSoup(urllib.request.urlopen('https://www.op.gg/summoner/userName=%EB%AD%90%ED%95%A0%EB%8B%89%EB%84%A4%EC%9E%84%EC%9D%B4%EC%97%86%EC%96%B4').read(), 'html.parser')
        to = soup.find_all('span', 'total')
        win = soup.find_all('span', 'total')
        lose = soup.find_all('span', 'total')
    
        for n in to:
            for n in win:
                for n in lose:
                    print(n.get_text())
                    await ctx.send(f"{n.get_text()}전")
def setup(bot):
    bot.add_cog(Player(bot))