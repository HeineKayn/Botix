import discord
from discord.ext import commands
from discord.utils import get
import asyncio

from datetime import datetime,timedelta
import typing
import json

#    Chaque donnée est stockées sous la forme : 
#    [
#      ["Serveur","Channel","User"],
#      "Date où doit ping",
#      "Date où memo crée",
#      "*args"
#    ]

def CroissFile(self,memo):
    file2 = []
    i = 0

    if len(self.File_Memo) == 0 :
        self.File_Memo.append(memo)

    else :
        for i,elem in enumerate(self.File_Memo) :
            if Get_Time(memo) < Get_Time(elem) :
                break

            file2.append(elem)
        self.File_Memo = file2 + [memo] + self.File_Memo[i+1:]

    with open(self.doc,'w') as outfile : 
        json.dump(self.File_Memo,outfile,indent=4)

def Get_Time(memo):
    date_string = memo[1]
    format_string = "%d/%m/%Y à %H:%M"
    return datetime.strptime(date_string,format_string)

def EqualTimes(t1,t2):
    return t1.strftime("%d/%m/%Y à %H:%M") == t2.strftime("%d/%m/%Y à %H:%M") # and abs(int(t1.strftime("%S")) - int(t2.strftime("%S"))) < 4

class MemoCog(commands.Cog): 

    def __init__(self,bot): 
        self.bot = bot
        self.format_string = "%d/%m/%Y à %H:%M"
        self.doc = "./annexes/memo.txt"

        try : 
            with open(self.doc,'r') as json_file:
                self.File_Memo = json.load(json_file)
        except :
            self.File_Memo = []

        async def MemoBackGround():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():

                if len(self.File_Memo) > 0 and EqualTimes(Get_Time(self.File_Memo[0]),datetime.now()):
                    infos = self.File_Memo[0][0]
                    guild = discord.utils.get(self.bot.guilds, id = infos[0])
                    channel = discord.utils.get(guild.channels, id = infos[1])
                    member = discord.utils.get(guild.members, id = infos[2])
                    horaire_creation = self.File_Memo[0][2]
                    args = self.File_Memo[0][3]

                    self.File_Memo.pop(0)
                    with open(self.doc,'w') as outfile : 
                        json.dump(self.File_Memo,outfile,indent=4)

                    await channel.send("**__Notification de {} créée le {}__**\n{}".format(member.mention,horaire_creation,' '.join(args)))

                await asyncio.sleep(1)

        self.bot.loop.create_task(MemoBackGround())

    def isowner(ctx):
        return ctx.message.author.id == 174112128548995072

########################################################################################################################
########################################################################################################################

    @commands.command(name='alerte',aliases=['alrt','al','bip'],help="-> Notifie un certains temps plus tard",hidden=True) # Rappelle un truc à une certaine date
    async def alerte(self,ctx, minutes : typing.Optional[int] = 0, heures : typing.Optional[int] = 0, jours : typing.Optional[int] = 0, *args):

        minutes = min(60,minutes)
        heures = min(24,heures)
        decal = datetime.now() + timedelta(minutes=minutes,hours=heures,days=jours) 

        infos_user = [ctx.message.guild.id,ctx.message.channel.id,ctx.message.author.id]
        decal_txt = decal.strftime("%d/%m/%Y à %H:%M")
        heure_txt = datetime.now().strftime("%d/%m/%Y à %H:%M")
        memo = [infos_user,decal_txt,heure_txt,args]

        CroissFile(self,memo)
        await ctx.send("Rappel enregistré. \nJe te notifierais le " + decal_txt)

########################################################################################################################
########################################################################################################################

    @commands.command(name='rappel',aliases=['remindme','memo','remind'],help="-> Notifie à une certaine date (exemple format : 2020-06-25 21:58)",hidden=True) # Rappelle un truc à une certaine date
    async def rappel(self,ctx, date = "", horaire = "", *args):

        try :
            format_string = "%d/%m/%Y %H:%M"
            date_string = date + " " + horaire 
            decal = datetime.strptime(date_string,format_string)

            infos_user = [ctx.message.guild.id,ctx.message.channel.id,ctx.message.author.id]
            decal_txt = decal.strftime("%d/%m/%Y à %H:%M")
            heure_txt = datetime.now().strftime("%d/%m/%Y à %H:%M")
            memo = [infos_user,decal_txt,heure_txt,args]

            CroissFile(self,memo)
            await ctx.send("Rappel enregistré. \nJe te notifierais le " + decal_txt)
            
        except : 
            await ctx.send("horaire invalide")

########################################################################################################################
########################################################################################################################

    @commands.command(name='memolist',aliases=['melist','mlst','tasks'],help="-> Montre toutes les notifs qui te concerne",hidden=True)
    async def memolist(self,ctx):
        user_tagged = "<@!" + str(ctx.message.author.id) + ">"
        role_tagged = ["<@&"+str(x.id)+">" for x in ctx.author.roles]
        role_tagged = set(role_tagged)

        concerne_list = [x for x in self.File_Memo if role_tagged.intersection(x[3]) or x[0][2] == ctx.message.author.id or user_tagged in x[3]]
        
        embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = "Notifications de " + ctx.message.author.name
            )
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        for concerne in concerne_list : 

            infos = concerne[0]
            guild = discord.utils.get(self.bot.guilds, id = infos[0])
            channel = discord.utils.get(guild.channels, id = infos[1])
            member = discord.utils.get(guild.members, id = infos[2])

            horaire_prevu = concerne[1]
            horaire_creation = concerne[2]
            args = concerne[3]

            embed.add_field(name = "Le __**{}**__ par __**{}**__ \n(Programmé le *{}*)".format(horaire_prevu,member.name,horaire_creation), inline=False, value = ' '.join(args))

        await ctx.send(embed=embed)

    @commands.command(name='removememo',aliases=['rmmemo','rmmm','rtask'],help="-> Supprime un memo prévu",hidden=True) 
    async def removememo(self,ctx,date = "", horaire = ""):

        count = 0

        try :
            format_string = "%d/%m/%Y %H:%M"
            date_string = date + " " + horaire 
            decal = datetime.strptime(date_string,format_string)
            decal_txt = decal.strftime("%d/%m/%Y à %H:%M")

            for memo in self.File_Memo : 

                infos = memo[0]
                guild = discord.utils.get(self.bot.guilds, id = infos[0])
                channel = discord.utils.get(guild.channels, id = infos[1])
                member = discord.utils.get(guild.members, id = infos[2])

                if member.id == ctx.message.author.id and decal_txt == memo[1] :

                    self.File_Memo.pop(count)

                    with open(self.doc,'w') as outfile : 
                        json.dump(self.File_Memo,outfile,indent=4)

                    count += 1

            if count == 0 :
                await ctx.send("Aucun memo correspondant à cette heure")
            else : 
                await ctx.send("{} memos ont été supprimés avec succès".format(count))


        except :
            await ctx.send("horaire invalide")

        


########################################################################################################################
########################################################################################################################  

def setup(bot):
    bot.add_cog(MemoCog(bot))