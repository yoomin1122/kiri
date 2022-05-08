
import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
from discord.ext.commands import CommandNotFound, has_permissions, MissingPermissions
import pytz
import traceback
from koreanbots.integrations.discord import DiscordpyKoreanbots
from discord.ext.commands import Bot
from discord_slash import SlashCommand


intents = discord.Intents.default()


bot = commands.Bot(command_prefix=["키리 ", "키리야 ", "키리", "키리야"], intents=intents)
slash = SlashCommand(bot, sync_commands=True)

for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")
        print(f"{filename[:-3]}가 로드되었습니다.")

@bot.event
async def on_ready():
    status = cycle(["http://kiribot.kro.kr", "키리야 명령어"])

    @tasks.loop(seconds=5)
    async def change_status():
        await bot.change_presence(activity=discord.Game(next(status)))

    change_status.start()
    print("ready")
    print(str(len(bot.guilds)) + "server join")

@bot.event
async def on_guild_join(guild):
     if guild.system_channel:
          embed = discord.Embed(color=0xfa4f4f)
          embed.set_author(name="안녕하세요 저는 키리에요!", icon_url="https://i.ibb.co/wpJj64Y/image.png")
          embed.add_field(name="개발자", value="> YooMin1122\n> <@433183785564110848>")
          embed.add_field(name="Kiri봇 설명", value="키리는 관리, 번역, 대화 등등 많은 기능이 있는 봇 입니다!", inline=False)
          embed.add_field(name="kiri 서포트 서버", value="[[참여하기]](https://discord.gg/B6MjFDjz23)")
          embed.add_field(name="kiri 초대링크", value="[[초대하기]](http://invite.jambot.kro.kr)")
          embed.add_field(name="서비스 이용 약관", value="[[확인하기]](https://wadeinteractive.net/terms)")
          embed.add_field(name="개인정보 보호정책", value="[[확인하기]](https://wadeinteractive.net/privacy)")
          await guild.system_channel.send(embed=embed)
          print(f"{guild.name}({guild.id})에 추가됨 현재 {len(bot.guilds)}서버에 있음")

@bot.event
async def on_guild_remove(guild):
    print(f"{guild.name}({guild.id})에서 추방당함 현재 {len(bot.guilds)}서버에 있음")

@bot.event
async def on_command_error(ctx, error):
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    err = [line.rstrip() for line in tb]
    errstr = '\n'.join(err)
    if isinstance(error, commands.NotOwner):
        await ctx.send('봇 주인만 사용 가능한 명령어입니다')
    elif isinstance(error, CommandNotFound): 
      await ctx.send("명령어가 없습니다!")
    elif isinstance(error, MissingPermissions):
        await ctx.send("서버 관리자가 아니여서 사용할수 없습니다!")


