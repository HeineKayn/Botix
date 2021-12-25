from quart import Blueprint, redirect

# ---------------

botixBP = Blueprint('botix', __name__, template_folder='templates', static_folder='static')

# ---------------

from .routes import communiquer
botixBP.register_blueprint(communiquer.commBP,url_prefix='/communiquer')

# ---------------

@botixBP.route("/")
async def hello():
    return redirect("/botix")