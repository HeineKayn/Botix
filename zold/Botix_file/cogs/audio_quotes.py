import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os 

import requests

import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re 

class Audio_Quotes_Cog(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    def isowner(ctx):
        return ctx.message.author.id == 174112128548995072

    @commands.command(name='quote',aliases=['q','cit','citation'],hidden=True) 
    async def quote(self,ctx,langue = "FR",champ = "",*args):

        if champ == "" :
            await ctx.send("Veuillez entrer un nom de champion")
        else :

            langue_list = ["FR","EN"]
            langue = process.extractOne(langue, langue_list)

            with open('./annexes/audio_quotes/Audio_' + langue[0] + '.txt') as json_file:
                data = json.load(json_file)

            champ_list = data.keys() 
            champ_tuple = process.extractOne(champ, champ_list)
            champ = champ_tuple[0]

            try : 
                citation = ' '.join(args)
                citation_list = data[champ].keys()
                citation_tuple = process.extractOne(citation, citation_list)
                citation = citation_tuple[0]

                audio = data[champ][citation]
                titre = re.sub("[^\w\s]", "", citation)[:220]
                path = './annexes/audio_quotes/' + titre + '.mp3'

                r = requests.get(audio, allow_redirects=True)
                open(path, 'wb').write(r.content)

                await ctx.send(file=discord.File(path))

                os.remove(path)

            except :
                await ctx.send("Désolé je n'ai pas trouvé de citation pour ce personnage")

    @commands.command(name='quote_list',aliases=['qlist','qli','ql','citl','citlist'],hidden=True) 
    async def quote_list(self,ctx,langue = "FR",champ = "",*args):

        if champ == "" :
            await ctx.send("Veuillez entrer un nom de champion")
        else :

            langue_list = ["FR","EN"]
            langue_tuple = process.extractOne(langue, langue_list)
            langue = langue_tuple[0]

            with open('./annexes/audio_quotes/Audio_' + langue + '.txt') as json_file:
                data = json.load(json_file)

            champ_list = data.keys() 
            champ_tuple = process.extractOne(champ, champ_list)
            champ = champ_tuple[0]

            if langue == "EN" :
                lien = "https://leagueoflegends.fandom.com/wiki/" + champ + "/Quotes"
            elif langue == "FR" :
                lien = "https://leagueoflegends.fandom.com/fr/" + champ + "/Historique"

            embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = lien
            )

            await ctx.send(embed = embed)

    @commands.command(name='quote_search',aliases=['qsearch','qse','qs','cits','citsearch'],hidden=True) 
    async def quote_search(self,ctx,langue = "FR",number = 3, *args):

        langue_list = ["FR","EN"]
        langue_tuple = process.extractOne(langue, langue_list)
        langue = langue_tuple[0]

        with open('./annexes/audio_quotes/Audio_' + langue + '.txt') as json_file:
            data = json.load(json_file)

        citation_liste = []
        for champion, citation_dic in data.items() :
            for citation in citation_dic.keys() :
                citation_liste.append(citation)

        match_list = process.extract(' '.join(args), citation_liste, limit=number)

        embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = "Citations ressemblantes"
        )

        for match_tuple in match_list : 
            for champion, citation_dic in data.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                for citation in citation_dic.keys() : 
                    if citation == match_tuple[0] :
                        embed.add_field(name = "{} ({}% ressemblant)".format(champion,match_tuple[1]), inline=False, value = match_tuple[0])

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Audio_Quotes_Cog(bot))