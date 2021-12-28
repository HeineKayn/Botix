from discord.ext import commands, ipc
import aiohttp

from .tools import *

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configPath = "../web_data/config.txt"

    @ipc.server.route()
    async def get_config(self,data):
        try : 
            with open(self.configPath) as json_file:
                config = json.load(json_file)
        except:
            config = {}
        return config

    @ipc.server.route()
    async def set_config(self,data):
        dic = data.config
        try : 
            with open(self.configPath) as json_file:
                config = json.load(json_file)

            for key,val in dic.items():
                if config[key] != val :
                    config[key] = val

                    if key == "pseudo":
                        await self.bot.user.edit(username=val)

                    elif key == "avatar":
                        async with aiohttp.ClientSession() as session:
                            async with session.get(val) as response:
                                img = await response.read()
                                await self.bot.user.edit(avatar=img)

            with open(self.configPath, 'w') as outfile:
                json.dump(config, outfile, indent=4)
        except:
            config = {}
        return config
            
def setup(bot):
    bot.add_cog(Config(bot))