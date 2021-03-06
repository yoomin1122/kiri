import re

import discord
import lavalink
from discord.ext import commands
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

url_rx = re.compile(r'https?://(?:www\.)?.+')


class LavalinkVoiceClient(discord.VoiceClient):
    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                    'localhost',
                    2333,
                    'youshallnotpass',
                    'us',
                    'default-node')
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        lavalink_data = {
                't': 'VOICE_SERVER_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        lavalink_data = {
                't': 'VOICE_STATE_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel)

    async def disconnect(self, *, force: bool) -> None:
        player = self.lavalink.player_manager.get(self.channel.guild.id)
        if not force and not player.is_connected:
            return
        await self.channel.guild.change_voice_state(channel=None)
        player.channel_id = None
        self.cleanup()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(936234465355780146)
            bot.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'eu', 'default-node')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('??????', 'play')

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('???????????? ????????? ?????????..??????')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('???????????? ????????? ????????? ?????? ?????????')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError('????????? `??????` ??? `?????????` ????????? ?????????..')

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('?????? ?????? ??????????????? ????????????!!')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)


    @cog_ext.cog_slash(name="play", description="???????????? ????????? ???????????????!",
        options=[create_option(name="query", description="?????? ????????? ???????????????", required=True, option_type=3)])
    async def _musicstart(self, ctx, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('????????? ????????????! ?????? ?????? ????????????.')

        embed = discord.Embed(color=discord.Color.blurple())
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
            embed.title = '????????? ???????????? ??????????????????'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed = discord.Embed(color=0xfa4f4f)
            embed.title = '????????? ???????????????'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)
        if not player.is_playing:
            await player.play()
            track = results['tracks'][0]
            embed = discord.Embed(color=0xfa4f4f)
            embed.title = '????????? ???????????????'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            await ctx.send(embed=embed)

    @commands.command(aliases=['p', 'play'])
    async def ??????(self, ctx : SlashContext, *, query:str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('????????? ????????????! ?????? ?????? ????????????.')

        embed = discord.Embed(color=discord.Color.blurple())
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
            embed.title = '????????? ???????????? ??????????????????'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed = discord.Embed(color=0xfa4f4f)
            embed.title = '????????? ???????????????'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['now', '????????????', '????????????', 'nowplaying'])
    async def ????????????(self, ctx):
        """ Shows the currently playing track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.current:
            return await ctx.send("????????? ???????????? ?????????")

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '???? LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        track = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=0xfa4f4f, title="?????? ???????????? ?????? ??????", description=track)

        if (currentTrackData := player.fetch("currentTrackData")) != None:
            embed.set_thumbnail(url=currentTrackData["thumbnail"]["genius"])
            embed.description += f"\n[LYRICS]({currentTrackData['links']['genius']})"

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="now", description="?????? ???????????? ????????? ???????????????",)
    async def _musicnow(self, ctx: SlashContext):
        """ Shows the currently playing track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send('???????????? ????????????')
        if not player.current:
            return await ctx.send("????????? ???????????? ?????????")

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '???? LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        track = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=0xfa4f4f, title="?????? ???????????? ?????? ??????", description=track)

        if (currentTrackData := player.fetch("currentTrackData")) != None:
            embed.set_thumbnail(url=currentTrackData["thumbnail"]["genius"])
            embed.description += f"\n[LYRICS]({currentTrackData['links']['genius']})"

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="stop", description="?????? ????????? ?????????",)

    async def _musicout(self, ctx: SlashContext):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send('???????????? ????????????')
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('?????? ?????? ??????????????? ????????????!!')
        player.queue.clear()
        await player.stop()
        await ctx.voice_client.disconnect(force=True)
        await ctx.send('??????????????? ???????????????')

    @commands.command(aliases=['dc', 'stop'])
    async def ??????(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('???????????? ????????????')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('?????? ?????? ??????????????? ????????????!!')
        player.queue.clear()
        await player.stop()
        await ctx.voice_client.disconnect(force=True)
        await ctx.send('??????????????? ???????????????')


    @cog_ext.cog_slash(name="skip", description="????????? ??????????????????",)
    async def _musicskip(self, ctx: SlashContext):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('???????????? ????????????')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('?????? ?????? ??????????????? ????????????!!')
        await player.skip()
        await ctx.send('????????? ?????????????????????')

    @commands.command(aliases=['sk', 'skip'])
    async def ??????(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('???????????? ????????????')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('?????? ?????? ??????????????? ????????????!!')
        await player.skip()
        await ctx.send('????????? ?????????????????????')

    @cog_ext.cog_slash(name="repeat", description="???????????????",)
    async def _musicrepeat(self, ctx: SlashContext):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('???????????? ????????????')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('?????? ?????? ??????????????? ????????????!!')
        player.repeat = not player.repeat

        await ctx.send('???????????????' + ('???????????????' if player.repeat else '???????????????'))

    @commands.command(aliases=['rep', 'repeat'])
    async def ??????(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('???????????? ????????????')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('?????? ?????? ??????????????? ????????????!!')
        player.repeat = not player.repeat

        await ctx.send('???????????????' + ('???????????????' if player.repeat else '???????????????'))


    @commands.command(aliases=['vol'])
    async def ??????(self, ctx, volume: int = None):
        """Changes the bot volume (1-100)."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'?????? ?????????`{player.volume * 2}%` ?????????')
        volume = max(1, min(volume, 100))

        await player.set_volume(volume / 2)
        await ctx.send(f'?????????`{player.volume * 2}%`??? ???????????????')

    @cog_ext.cog_slash(name="volume", description="???????????????",)
    async def _musicvolume(self, ctx: SlashContext, volume : int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not volume:
            return await ctx.send(f'?????? ?????????`{player.volume * 2}%` ?????????')
        volume = max(1, min(volume, 100))
        await player.set_volume(volume / 2)
        await ctx.send(f'?????????`{player.volume * 2}%`??? ???????????????')
def setup(bot):
    bot.add_cog(Music(bot))
