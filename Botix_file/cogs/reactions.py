import discord
from discord.ext import commands
from discord.utils import get
import asyncio

class ReactCog(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        # ----------------- Modifiable
        self.guild = discord.utils.get(self.bot.guilds, name="bdo")
        self.channel = discord.utils.get(self.guild.channels, name="annonces") 
        self.emoji = "👍"
        self.role = "Participe"
        # -----------------
        self.original_id = self.channel.last_message_id
         

    async def React_Role(self,payload,adding):
        original = await self.channel.fetch_message(self.original_id)

        user_id = payload.user_id
        reacted_message_id = payload.message_id
        emoji = payload.emoji

        member = self.guild.get_member(user_id)
        if reacted_message_id == self.original_id and str(emoji) == self.emoji:
            role = discord.utils.get(self.guild.roles,name=self.role)
            if adding:
                await member.add_roles(role)
            if not adding:
                await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        await self.React_Role(payload,True)
                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        await self.React_Role(payload,False)

def setup(bot):
    bot.add_cog(ReactCog(bot))