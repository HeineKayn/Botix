from quart import Quart, redirect
import os

# ---------------

from dotenv import load_dotenv

load_dotenv()
app_pass = os.getenv('APP_Pass')

# ---------------

app = Quart(__name__, static_folder = None)

from quart_auth import *

auth_manager = AuthManager(app)
app.secret_key = app_pass 
app.config.from_mapping(QUART_AUTH_COOKIE_HTTP_ONLY = False)
app.config.from_mapping(QUART_AUTH_COOKIE_SECURE    = False)
app.config.from_mapping(QUART_AUTH_COOKIE_SECURE    = False)

# ---------------

from botix import botixBP
app.register_blueprint(botixBP,url_prefix='/botix')

# ---------------

# Default route
@app.route("/")
def default():
	return redirect("/botix")

# ---------------

if __name__ == "__main__":
	app.run(host="localhost", port=5000, debug=True)