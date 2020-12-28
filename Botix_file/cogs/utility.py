import discord
from discord.ext import commands
from discord.utils import get
import asyncio

liens = {
    "site" : "http://demacia.fr/",
    "serment" : "https://docs.google.com/document/d/1-Yk4mgFttjCQMIctKLq8U_B4r8jLBF8M8mN085Nnrs0/edit?usp=sharing",
    "maisons" : "https://docs.google.com/document/d/19EB6HEkQ0utrKXC_sE2w6NEQtmTfk23I4fWAoZYL3P0/edit?usp=sharing",
    "guide" : "https://docs.google.com/document/d/1OOC4xFVGvMgZLhCNgHRqwvk8WsC6n_iHhL-ajC6gwpA/edit?usp=sharing",
    "mundo" : "https://docs.google.com/document/d/1GnjVhMfKWWyjOFq6wg1nNQigAL7j-T_xEGEUv1WF8Ds/edit?usp=sharing",

    "sketch" : "https://docs.google.com/document/d/1CoK23txxQY4cCrq7qObg3nCb22GWw92kHLYT0lMVHjU/edit?usp=sharing",
    "tokor" : "https://drive.google.com/file/d/1isKoEpFKycOmrjjHRQ1t4mKSyzldXBPr/view?usp=sharing",
    "asheraly" : "https://drive.google.com/file/d/1zrNfJtTJejgfRaUUmujraIVdrWUvTm9c/view?usp=sharing",
    "charon" : "https://drive.google.com/file/d/14N9gCs7Trq3HdkMBAVmNcLnvYoB8QbQt/view?usp=sharing",
    "lunny" : "https://drive.google.com/file/d/166GzZIb1ANuP8LFbzECkz4nFANBoIS2W/view?usp=sharing",
    "ouria" : "https://drive.google.com/file/d/1UarjNgOrcSd_fMHZTNjWX4NeejXJRCEs/view?usp=sharing",
 }

class UtilityCog(commands.Cog):

    def __init__(self,bot):
        self.liens = liens
        self.bot = bot

    def isowner(ctx):
        return ctx.message.author.id == 174112128548995072

    def noban(ctx):
        return ctx.message.author.id not in banlist

    @commands.command(name='doc',aliases=['lien','liens','docs'],hidden=True)
    async def doc(self,ctx,key):
        key = key.lower()
        if key == "help" or "":
            await ctx.send("Documents : {}".format(', '.join(liens.keys())))
        elif key in liens.keys():
            await ctx.send(liens[key])
        else:
            await ctx.send("Ce document n'existe pas :/")

    @commands.command(name='ping',hidden=True)
    async def ping(self,ctx):
        ping_ = bot.latency
        ping =  round(ping_ * 1000)
        await ctx.send(f"my ping is {ping}ms")


    @commands.command(name='dice',aliases=['chance','luck'], help='-> Dame chance nous sourit\n(max des = 10, max cotes = 20)',hidden=True) # Lance nd dès à nc faces 
    async def roll(self,ctx, nombre_de_des: int, nombre_de_côtes: int):
        nd = min(nombre_de_des,10)
        nc = min(nombre_de_côtes,20)
        dès = [
            str(random.choice(range(1, nc + 1)))
            for _ in range(nd)
        ]
        await ctx.send(', '.join(des))

def setup(bot):
    bot.add_cog(UtilityCog(bot))