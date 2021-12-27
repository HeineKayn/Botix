from discord.ext import commands, ipc

class Communiquer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def get_member_count(self, data):
        guild = await self.bot.fetch_guild(data.guild_id)  # get the guild object using parsed guild_id
        return guild.name  # return the member count to the client

def setup(bot):
    bot.add_cog(Communiquer(bot))