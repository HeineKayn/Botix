import discord
from discord.ext import commands
from discord.utils import get
import asyncio

import os 
import youtube_dl
from discord import FFmpegPCMAudio

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Bot_ActCog(commands.Cog):

    def __init__(self,bot):
        self.selected = None
        self.bot = bot

    def isowner(ctx):
        return ctx.message.author.id == 174112128548995072

    @commands.command(name='select',aliases=['sel','choose'],hidden=True) 
    async def select(self,ctx,guildname="",channelname=""):

        try :
            guild_list = [x.name for x in self.bot.guilds]
            match_guild = process.extractOne(guildname, guild_list)
            if match_guild[1] > 80 : 
                guildname = match_guild[0]
                guild = discord.utils.get(self.bot.guilds, name=guildname)

                channel_list = [x.name for x in guild.channels]
                try :

                    match_channel = process.extractOne(channelname, channel_list)
                    if match_channel[1] > 80 : 
                        channelname = match_channel[0]
                        self.selected = discord.utils.get(guild.channels, name=channelname) 
                        await ctx.send("Channel selectionné :white_check_mark:")

                except :
                    await ctx.send("Channel inexistant")

        except : 
            await ctx.send("Serveur inexistant")
            

    @commands.command(name='botsay',aliases=['puppet','bsay'],hidden=True) 
    async def botsay(self,ctx,*args):
        try:
            await self.selected.send(' '.join(args))
        except:
            await ctx.send("Aucun channel selectionné")

    @commands.command(name='botdm',hidden=True) 
    @commands.check(isowner)
    async def botdm(self,ctx,member: discord.Member,*args):
        try : 
            await member.send(' '.join(args))
        except : 
            await ctx.send("Utilisateur invalide ou non présent sur le serveur")

    @commands.command(name='type',aliases=['ty','fake'],hidden=True) 
    @commands.check(isowner)
    async def type(self,ctx,time=10):
        try : 
            async with self.selected.typing():
               await asyncio.sleep(time)
        except :
            await ctx.send("Aucun channel selectionné")

def setup(bot):
    bot.add_cog(Bot_ActCog(bot))