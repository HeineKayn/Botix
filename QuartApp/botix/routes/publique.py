from quart import Blueprint, render_template, redirect, url_for
from quart_auth import *

from .tools.contextGetter import *
from .tools.messageGetter import *

publiqueBP = Blueprint('publique', __name__)

@publiqueBP.route("/")
async def place_publique():

    app = current_app.config["ipc_client"]
    guild = "bdo" # "The Kingdom Of Demacia"
    channel = "🏰place_publique" 

    messages = await get_last_messages(app,guild,channel,100)
    demaciens = await get_demaciens(app,guild,channel)

    return await render_template('place_publique.html',messages=messages, demacien_list=demaciens)
