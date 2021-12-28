from discord.ext import commands
from discord.utils import get

import json
import random

class DM_Response(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):

        try : 
            with open("../web_data/config.txt") as json_file:
                reponse = json.load(json_file)["reponse"]
                reponse = reponse.split("\n")
        except :
            reponse = ""

        if not message.guild and not message.author.bot : 
            await message.author.send(random.choice(reponse))


def setup(bot):
    bot.add_cog(DM_Response(bot))