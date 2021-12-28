from quart import Blueprint, current_app, render_template
from quart_auth import *

from .tools.contextGetter import *
from .tools.messageGetter import *

commBP = Blueprint('communiquer', __name__)

@commBP.route('/')
async def index():
    app = current_app.config["ipc_client"]
    guild_list = await get_guilds(app)
    return await render_template('communiquer.html',guild_list=guild_list)

@commBP.route("/select_guild", methods=['POST'])
@login_required
async def select_guild():
    app = current_app.config["ipc_client"]
    req = await request.form

    selected_guild = req["guild"]
    guild_list = await get_guilds(app)
    channel_list = []
    for guild in guild_list :
        if selected_guild == guild["name"]:
            channel_list = await get_channels(app,selected_guild)
            break
    return {"channel_list" : channel_list}

@commBP.route("/select_channel", methods=['POST'])
@login_required
async def select_channel():
    app = current_app.config["ipc_client"]
    req = await request.form

    guild = req["guild"]
    channel = req["channel"]
    messages = await get_last_messages(app,guild,channel,100)

    # Changer au lieu de renvoyer des messages on renvoie le bout de code qui y'a dans place publique
    # un peu à la manière de logs pour bravery
    return {"messages" : messages}

@commBP.route("/send_message", methods=['POST'])
@login_required
async def send_message():
    app = current_app.config["ipc_client"]
    req = await request.form
    
    await app.request("send_message",guild=req["guild"],channel=req["channel"],message=req["content"])
    return {}