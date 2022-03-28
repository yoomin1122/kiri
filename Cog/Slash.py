import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import  create_actionrow, create_button
from discord_slash.model import ButtonStyle
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
import translatetool

class Slsh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slash(self, ctx):
        await ctx.send("개발봇 Cogs/Slash.py 출력완료")
    @cog_ext.cog_slash(name="test", guild_ids=[918171855418982410])
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="Embed Test")
        await ctx.send(embed=embed)
 
    @cog_ext.cog_slash(name="swa", guild_ids=[918171855418982410])
    async def wa(self, ctx: SlashContext):
        buttons = [
            create_button(style=ButtonStyle.green, label="A green button"),
            create_button(style=ButtonStyle.blue, label="A blue button")
        ]
        action_row = create_actionrow(*buttons)

        await ctx.send(components=[action_row])

def setup(bot):
    bot.add_cog(Slsh(bot))
