import discord
from datetime import datetime
from discord.ext import commands, ipc

from .tools import *

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def send_message(self,data):
        guild = discord.utils.get(self.bot.guilds, name = data.guild)
        channel = discord.utils.get(guild.channels, name = data.channel)
        await channel.send(data.message)

    @ipc.server.route()
    async def get_last_messages(self,data):
        limit         = data.limit
        server_name   = data.server        
        channel_name  = data.channel

        file = "messages/{}/{}.txt".format(server_name,channel_name)

        try : 
            guild   = discord.utils.get(self.bot.guilds, name = server_name)
            channel = discord.utils.get(guild.channels, name = channel_name)

            historique = []
            messages = await channel.history(limit=limit).flatten()
            for message in messages:
                histo_dic                = {}
                histo_dic["avatar"]        = str(message.author.avatar_url)
                histo_dic["name"]        = message.author.name
                histo_dic["content"]    = [message.clean_content]
                histo_dic["colour"]         = str(message.author.colour)

                histo_dic["attachements"] = []
                for attach in message.attachments :

                    attach_dic             = {}
                    attach_dic["name"]     = attach.filename
                    attach_dic["url"]     = attach.url
                    histo_dic ["attachements"].append(attach_dic) 

                decal_today = (datetime.now() - message.created_at).days
                if decal_today == 0 :
                    date = message.created_at.strftime("Aujourd'hui à %H:%M")
                elif decal_today == 1:
                    date = message.created_at.strftime("Hier à %H:%M")
                elif decal_today == 2:
                    date = message.created_at.strftime("Avant-hier à %H:%M")
                else :
                    date = message.created_at.strftime("%d/%m/%Y")

                histo_dic["date"] = date
                historique.append(histo_dic)

            Update_json(file,historique)

        except:
            pass

def setup(bot):
    bot.add_cog(Message(bot))