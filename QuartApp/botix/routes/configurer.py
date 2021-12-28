from quart import Blueprint, render_template
from quart_auth import *

import json
import random

configBP = Blueprint('config', __name__)

keyPath = './QuartApp/botix/static/keys.txt'

@configBP.route("/")
@login_required
async def config():
	app = current_app.config["ipc_client"]
	config = await app.request("get_config")
	return await render_template('config.html',config=config)

@configBP.route("/config_element", methods=['POST'])
@login_required
async def config_element():
	app = current_app.config["ipc_client"]
	req = await request.form

	dic = {req["name"] : req["value"]}
	await app.request("set_config",config=dic)
	return {}

@configBP.route("/generate_key", methods=['POST'])
@login_required
async def generate_key():
	req = await request.form
	nb = int(req["number"])

	try : 
		with open(keyPath) as json_file:
			keys = json.load(json_file)	
	
	except : 
		keys = []

	for i in range(nb):
		key = ""
		possible = list(range(48,58)) + list(range(65,91))
		for i in range(4):
			for j in range(4):
				key += chr(random.choice(possible))
			key += "~"
		key = key[:-1]
		keys.append(key)

	try :
		with open(keyPath, 'w') as outfile:
			json.dump(keys, outfile, indent=4)
	except:
		pass

	return {"generated" : nb}