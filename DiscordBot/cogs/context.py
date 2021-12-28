import discord
from datetime import datetime
from discord.ext import commands, ipc

from .tools import *

class Context(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def get_guilds(self,data):
        file = "guilds.txt"

        guilds = []
        for guild in self.bot.guilds :
            guild_dic		  = {}
            guild_dic["name"] = guild.name
            guild_dic["icon"] = str(guild.icon_url)
            if not guild.icon :
                guild_dic["icon"] = "https://cdn.discordapp.com/attachments/267700847398486018/813560519520026704/default_server.png"
            guilds.append(guild_dic)

        Update_json(file,guilds)
            

    @ipc.server.route()
    async def get_channels(self,data):
        server_name  = data.server
        file = "guilds/{}.txt".format(server_name)

        try : 
            guild   = discord.utils.get(self.bot.guilds, name = server_name)
            channels = []
            for channel in guild.text_channels : 
                channels.append(channel.name)

            Update_json(file,channels)

        except : 
            pass

    @ipc.server.route()
    async def get_demaciens(self,data):
        server_name  = data.server 
        channel_name = data.channel 

        maisons = ["Vayne","Buvelle","Crownguard","Laurent","Cloudfield"]
        demaciens = {}

        file = "demaciens/{}/{}.txt".format(server_name,channel_name)

        try :  
            guild   = discord.utils.get(self.bot.guilds, name = server_name)
            channel = discord.utils.get(guild.channels, name = channel_name)
            role = discord.utils.get(guild.roles, name = "Demacien")

            members = [x for x in channel.members if role in x.roles]
            for member in members:

                demacien_dic			= {}
                demacien_dic["avatar"]	= str(member.avatar_url)
                demacien_dic["name"]	= member.name
                demacien_dic["name_id"]	= "{} - {}".format(member.name,member.id)
                demacien_dic["status"]	= member.raw_status
                demacien_dic["colour"]	= str(member.colour)
                
                try :
                    maison  = [str(x) for x in member.roles if str(x) in maisons][0]
                except :
                    maison = "Demacien"

                if maison in demaciens:
                    demaciens[maison] += [demacien_dic]
                else : 
                    demaciens[maison] = [demacien_dic]

            Update_json(file,demaciens)

        except : 
            pass

def setup(bot):
    bot.add_cog(Context(bot))