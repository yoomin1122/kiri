import os
from pydoc import describe

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, has_permissions
import random
import time
import datetime
import traceback
from discord_slash import SlashCommand

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def admin(self, ctx):
        await ctx.send("개발봇 Cogs/Admin.py 출력완료")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 청소(self, ctx, number: int = None):
        if ctx.guild:
            if ctx.message.author.guild_permissions.manage_messages:
                try:
                    if number is None:
                        await ctx.reply('숫자를 입력해주세요.')
                    elif 100 < number:
                        await ctx.message.delete()
                        await ctx.send(f'{ctx.message.author.mention} 100보다 큰 수는 입력할 수 없습니다.', delete_after=5)
                    else:
                        deleted = await ctx.message.channel.purge(limit=number)
                        embed = discord.Embed(title="청소 완료",description=f"청소된 메세지 : {len(deleted)}개",  color = 0xfa4f4f)
                        embed.set_footer(text=f"청소한 관리자 : {ctx.message.author.name}")
                        await ctx.send(embed=embed)
                except:
                    await ctx.reply("삭제가 불가합니다.")
            else:
                await ctx.reply('이 명령을 사용할 수 있는 권한이 없습니다.')
        else:
            await ctx.reply('DM에선 불가합니다.')

    @commands.command(aliases=["kick"])
    @commands.has_permissions(kick_members=True)
    async def 킥(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'유저 {member}을(를) 내보냈습니다. \n사유 : {reason}')

    @commands.command(aliases=["ban", "차단"])
    @commands.has_permissions(kick_members=True)
    async def 밴(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'유저 {member}을(를) 차단하였습니다.')

    @commands.command()
    async def 뮤트(self, ctx, member: discord.Member, minutes: int):
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)
        await ctx.reply(f"해당유저를 {minutes}분동안 뮤트를 시켰습니다.")
        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(until)

    @commands.command(aliases=['해제'])
    @commands.has_permissions(kick_members=True)
    async def 언밴(self, ctx, nickname: str):
        ban_entry = await ctx.guild.bans()
        for users in ban_entry:
            if nickname == users.user.name:
                forgive_user = users.user
                await ctx.guild.unban(forgive_user)
                return await ctx.send(f"{nickname} 님이 차단 해제되었습니다.")
        return await ctx.send(f"{nickname} 님은 차단 목록에 없습니다.")

def setup(bot):
    bot.add_cog(Admin(bot))
