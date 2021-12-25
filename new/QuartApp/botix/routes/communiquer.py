from quart import Blueprint, current_app

commBP = Blueprint('communiquer', __name__)

@commBP.route('/')
async def index():
    guild_name = await current_app.config["ipc_client"].request("get_member_count", guild_id=663392854273556490)   
    return guild_name 
    # return render_template('communiquer.html')