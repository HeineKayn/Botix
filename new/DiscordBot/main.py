import discord
from discord.ext import commands, ipc

import os 
from dotenv import load_dotenv

load_dotenv()

# --------------

IPC_Pass = os.getenv('IPC_Pass')
Token = os.getenv('Test_Token')

# --------------

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key=IPC_Pass)  # create our IPC Server
        self.load_extension("cogs.ipc")  # load the IPC Route cog

    async def on_ready(self):
        print("Bot is ready.")

    async def on_ipc_ready(self):
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)


my_bot = MyBot(command_prefix="!", intents=discord.Intents.all())

# --------------

if __name__ == "__main__":
	my_bot.ipc.start()  # start the IPC Server
	my_bot.run(Token,bot=True)
