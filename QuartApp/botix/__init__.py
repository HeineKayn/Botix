from quart import Blueprint, redirect

# ---------------

botixBP = Blueprint('botix', __name__, template_folder='templates', static_folder='static')

# ---------------

from .routes import communiquer
botixBP.register_blueprint(communiquer.commBP,url_prefix='/communiquer')

from .routes import login
botixBP.register_blueprint(login.loginBP,url_prefix='/login')

from .routes import fortune
botixBP.register_blueprint(fortune.fortuneBP,url_prefix='/fortune')

# ---------------

@botixBP.route("/")
async def hello():
    return redirect("/botix")