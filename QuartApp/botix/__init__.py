from quart import Blueprint, redirect

# ---------------

botixBP = Blueprint('botix', __name__, template_folder='templates', static_folder='static')

# ---------------

from .routes.publique import publiqueBP
botixBP.register_blueprint(publiqueBP,url_prefix='/place_publique')

from .routes.communiquer import commBP
botixBP.register_blueprint(commBP,url_prefix='/communiquer')

from .routes.login import loginBP
botixBP.register_blueprint(loginBP,url_prefix='/login')

from .routes.fortune import fortuneBP
botixBP.register_blueprint(fortuneBP,url_prefix='/fortune')

from .routes.configurer import configBP
botixBP.register_blueprint(configBP,url_prefix='/config')

# ---------------

@botixBP.route("/")
async def hello():
    return redirect("/botix/place_publique")