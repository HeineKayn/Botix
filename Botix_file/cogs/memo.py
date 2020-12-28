import discord
from discord.ext import commands
from discord.utils import get
import asyncio

from datetime import datetime,timedelta
import typing
import json

# ---------------

import aiomysql
import sys
import os 

# ---------------

def Content_Mention(Content,channel): # transforme les @Deltix ou @Demacien en mention 
    Content = Content.split()
    for i,word in enumerate(Content) :
        if word[0] == "@" :
            word = word[1:]

            try :
                Content[i] = discord.utils.get(channel.members, name = word).mention
            except:
                pass

            try :
                Content[i] = discord.utils.get(channel.guild.roles, name = word).mention
            except:
                pass

    return " ".join(Content)


class MemoCog(commands.Cog): 

    def __init__(self,bot): 
        self.bot = bot
        self.format_string_User = "%d/%m/%Y à %H:%M"    # Quand on montre à l'User
        self.format_string_DB = "%Y/%m/%d %H:%M"        # Quand on met dans la DB
        self.format_string_DBUser = "%Y/%m/%d à %H:%i"  # Quand ça sort de la DB

        async def MemoBackGround():
            await self.bot.wait_until_ready()

            Q_isTime = """
                        SELECT 
                            DATE_FORMAT(DateCreated,%s), 
                            DATE_FORMAT(DatePlanned,%s), 
                            idGuild, idChannel, idInvoker, Content 
                        FROM Horaire 
                        INNER JOIN Info
                            ON Horaire.ID = Info.idHoraire
                        WHERE 
                            TIMESTAMPDIFF(MINUTE,NOW(),DatePlanned) < 1
                        ORDER BY DateCreated ASC
                       """

            Q_Delete = """
                        DELETE        
                        FROM Horaire
                        WHERE 
                            TIMESTAMPDIFF(MINUTE,NOW(),DatePlanned) < 1
                       """

            DBUser = self.format_string_DBUser

            while not self.bot.is_closed():
                await self.bot.cur.execute(Q_isTime,(DBUser,DBUser))
                ready_list = await self.bot.cur.fetchall()

                for ready in ready_list : 

                    (DateCreated, DatePlanned, idGuild, idChannel, idInvoker, Content) = ready
                    guild = discord.utils.get(self.bot.guilds, id = idGuild)
                    channel = discord.utils.get(guild.channels, id = idChannel)

                    try :
                        member_name = discord.utils.get(guild.members, id = idInvoker).mention
                    except:
                        member_name = "?"  

                    Content = Content_Mention(Content,channel)

                    await channel.send("**Notification de {} créée le __{}__**\n{}".format(member_name,DateCreated,Content))

                await self.bot.cur.execute(Q_Delete)
                await self.bot.cur.execute("COMMIT")
                await asyncio.sleep(30)

        self.bot.loop.create_task(MemoBackGround())

        #################

    async def Insert_Request(self,message,str_format,decal,args):

        (idMessage,idGuild,idChannel,idInvoker) = (message.id,message.guild.id,message.channel.id,message.author.id)
        DateCreated = datetime.now().strftime(str_format)
        DatePlanned = decal.strftime(str_format)

        nb_args = len(args)
        args = message.clean_content
        args = args.split()[-nb_args:]
        Content = " ".join(args)

        Q_Add_Horaire = "INSERT INTO Horaire (DateCreated,DatePlanned) VALUES (%s,%s)"
        Q_Add_Requete = """INSERT INTO Info (idMessage, idHoraire, idGuild, idChannel, idInvoker, Content) 
                           VALUES (%s,(SELECT ID FROM Horaire WHERE DateCreated = %s and DatePlanned = %s),%s,%s,%s,%s)"""

        try :
            await self.bot.cur.execute(Q_Add_Horaire,(DateCreated,DatePlanned))
        except:
            print("Doublon")

        await self.bot.cur.execute(Q_Add_Requete,(idMessage,DateCreated,DatePlanned,idGuild,idChannel,idInvoker,Content))
        await self.bot.cur.execute("COMMIT")


    @commands.command(name='alerte',aliases=['alrt','al','bip'],help="-> Notifie un certains temps plus tard",hidden=True) # Rappelle un truc à une certaine date
    async def alerte(self,ctx, minutes : typing.Optional[int] = 0, heures : typing.Optional[int] = 0, jours : typing.Optional[int] = 0,*args):

        minutes = min(60,minutes)
        heures = min(24,heures)
        decal = datetime.now() + timedelta(minutes=minutes,hours=heures,days=jours) 

        await self.Insert_Request(ctx.message,self.format_string_DB,decal,args)
        await ctx.send("Rappel enregistré. \nJe te notifierais le " + decal.strftime(self.format_string_User))

    @commands.command(name='rappel',aliases=['remindme','memo','remind'],help="-> Notifie à une certaine date (exemple format : 2020/06/25 21:58)",hidden=True) # Rappelle un truc à une certaine date
    async def rappel(self,ctx, date = "", horaire = "", *args):

        try :
            date_string = date + " " + horaire 
            decal = datetime.strptime(date_string,self.format_string_DB) # Si le format n'est pas valide on sort du try

            await self.Insert_Request(ctx.message,self.format_string_DB,decal,args)
            await ctx.send("Rappel enregistré. \nJe te notifierais le " + decal.strftime(self.format_string_User))
            
        except : 
            await ctx.send("Horaire invalide, respectez le format 2020/06/25 21:58")

    @commands.command(name='memolist',aliases=['melist','mlst','tasks'],help="-> Montre toutes les notifs qui te concerne",hidden=True)
    async def memolist(self,ctx):

        author_tagged = "@" + str(ctx.message.author.name)
        role_tagged = ["@"+str(x.name) for x in ctx.author.roles]
        concerne = role_tagged + [author_tagged]

        Q_Memo = """
                    SELECT 
                        DATE_FORMAT(DateCreated,%s), 
                        DATE_FORMAT(DatePlanned,%s), 
                        idGuild, idChannel, idInvoker, Content, idMessage
                    FROM Horaire 
                    INNER JOIN Info
                    ON Horaire.ID = Info.idHoraire
                    WHERE 
                        idInvoker = (%s) OR 
                        {}
                    ORDER BY DatePlanned ASC
                 """

        Format_LIKE = "Content LIKE '%%{}%%'"
        concerne = [Format_LIKE.format(x) for x in concerne]
        concerne = " OR ".join(concerne)
        Q_Memo = Q_Memo.format(concerne)

        DBUser = self.format_string_DBUser
        await self.bot.cur.execute(Q_Memo,(DBUser,DBUser,ctx.author.id,)) # peut être add virgule après
        query_result = await self.bot.cur.fetchall()

        embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = "Notifications de " + ctx.message.author.name
            )
        embed.set_thumbnail(url=ctx.message.author.avatar_url)

        for result in query_result : 

            (DateCreated, DatePlanned, idGuild, idChannel, idInvoker, Content, idMessage) = result
            guild = discord.utils.get(self.bot.guilds, id = idGuild)
            channel = discord.utils.get(guild.channels, id = idChannel)

            try :
                member_name = discord.utils.get(guild.members, id = idInvoker).name
            except:
                member_name = "?" 

            Content = Content_Mention(Content,channel)

            embed.add_field(name = "__Le {} par {}__".format(DatePlanned,member_name), 
                            inline=False, 
                            value = "Programmé le __{}__\n*Id Message : {}*\n**{}**".format(DateCreated,idMessage,Content))

        await ctx.send(embed=embed)

    @commands.command(name='removememo',aliases=['rmmemo','rmemo','rmo'],help="-> Supprime les mémos contenus qui ont été crée par les id des messages en argument",hidden=True)
    async def removememo(self,ctx,*args):

        invalid_list = []

        Q_Remove = """
                    DELETE h 
                    FROM Horaire h 
                    INNER JOIN Info i 
                        ON h.ID = i.idHoraire 
                    WHERE 
                        i.idMessage = (%s)
                    """

        if len(args) < 10 and len(args) > 0: 

            for c,idMessage in enumerate(args) :
                try :
                    message = await ctx.channel.fetch_message(int(idMessage))
                    await self.bot.cur.execute(Q_Remove,(idMessage,))
                except :
                    invalid_list.append(str(c+1))

            if invalid_list :
                await ctx.send("Les arguments {} ne sont pas valides".format(" ".join(invalid_list)))
            else :
                await ctx.send("Tous les mémos ont été supprimés avec succès")


def setup(bot):
    bot.add_cog(MemoCog(bot))