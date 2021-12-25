from discord.ext.ipc import Client
from quart import Blueprint

import os

ipc_pass = os.getenv('IPC_Pass')
ipc_client = Client(secret_key = ipc_pass)

# ---------------

botixBP = Blueprint('botix', __name__, template_folder='templates', static_folder='static')

# ---------------

@botixBP.route("/")
async def hello():
    guild_name = await ipc_client.request("get_member_count", guild_id=663392854273556490)     
    return guild_name  # display member count