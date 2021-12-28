import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os 

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

class Scrapper1_Cog(commands.Cog):

    def __init__(self,bot):
        self.url = 'http://demacia.fr/'
        self.bot = bot

    def isowner(ctx):
        return ctx.message.author.id == 174112128548995072

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    @commands.command(name='select',aliases=['sel','choose'],hidden=True) 
    @commands.check(isowner)

def setup(bot):
    bot.add_cog(Scrapper1_Cog(bot))