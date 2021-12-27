import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os 
import youtube_dl


class AudioCog(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    def isowner(ctx):
        return ctx.message.author.id == 174112128548995072

    @commands.command(pass_context=True,hidden=True)
    @commands.check(isowner)
    async def join(self,ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(pass_context=True,hidden=True)
    @commands.check(isowner)
    async def pause(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_paused():
            await voice.pause()

    @commands.command(pass_context=True,hidden=True)
    @commands.check(isowner)
    async def resume(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await voice.resume()

    @commands.command(pass_context=True,hidden=True)
    @commands.check(isowner)
    async def stop(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await voice.stop()

    @commands.command(pass_context=True,hidden=True)
    @commands.check(isowner)
    async def leave(self,ctx):
        voice_bot = ctx.message.guild.voice_client
        await voice_bot.disconnect()

    @commands.command(name="musiclist",aliases = ["ml","mlist"],pass_context=True,hidden=True)
    @commands.check(isowner)
    async def musiclist(self,ctx):
        dir = os.listdir("./annexes/musiques")
        await ctx.send('Musiques déjà présentes :\n{}'.format(', '.join(dir)))

    @commands.command(name="musicbomb", aliases=["mb","bomb"],hidden=True)
    @commands.check(isowner)
    async def musicbomb(self,ctx,member, source: str):
        source = "./annexes/musiques/" + source + ".mp3"
        if os.path.isfile(source):
            guild = ctx.guild
            member = discord.utils.get(guild.members, name=member)
            channel = member.voice.channel
            voice_bot = guild.voice_client
            await channel.connect()
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            await voice.play(discord.FFmpegPCMAudio(source),after = lambda x : asyncio.run_coroutine_threadsafe(ctx.message.guild.voice_client.disconnect(),ctx.message.guild.voice_client.loop))
        else:
            await ctx.send("Cette musique n'est pas présente dans le dossier")

    @commands.command(name="dlmusic", aliases=["dlm"], hidden=True)
    @commands.check(isowner)
    async def dlmusic(self,ctx,url: str, nom: str):
        nom += ".mp3"
        ydl_opts = {
            'outtmpl': 'annexes/musiques/' + nom,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        if os.path.isfile(nom):
            os.remove(nom)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def setup(bot):
    bot.add_cog(AudioCog(bot))