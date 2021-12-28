from quart import Blueprint, render_template, redirect
from quart_auth import *

import json
import random

fortuneBP = Blueprint('fortune', __name__)

coffrePath = './QuartApp/botix/static/coffres.txt'
keyPath    = './QuartApp/botix/static/keys.txt'

@fortuneBP.route("/")
@login_required
async def fortune():
	try : 
		with open(coffrePath) as json_file:
			coffres = json.load(json_file)
	except : 
		coffres = []

	try : 
		with open(keyPath) as json_file:
			keys = json.load(json_file)
	except : 
		keys = []
		
	return await render_template('fortune.html',coffres=coffres,keys=keys)

# Si on vient en cliquant sur le menu on mélange l'ordre des coffres
@fortuneBP.route("/first-time")
@login_required
async def fortune_shuffle():
	try : 
		with open(coffrePath) as json_file:
			coffres = json.load(json_file)
			random.shuffle(coffres)

		with open(coffrePath, 'w') as outfile:
			json.dump(coffres, outfile, indent=4)
	except : 
		pass
	return redirect("/botix/fortune")

@fortuneBP.route('/open', methods=['POST'])
@login_required
async def fortune_open():
	id_coffre = await request.form
	id_coffre = int(id_coffre['id_coffre']) - 1

	try : 
		with open(coffrePath) as json_file:
			coffres = json.load(json_file)
			coffres[id_coffre]["open"] = True

		with open(coffrePath, 'w') as outfile:
			json.dump(coffres, outfile, indent=4)

	except : 
		pass

	return {"content" : coffres[id_coffre]["content"]}

@fortuneBP.route('/use_key', methods=['POST'])
@login_required
async def use_key():
	key_exist = False
	key = await request.form
	key = key['key']

	try : 
		with open(keyPath) as json_file:
			coffres = json.load(json_file)

		key_exist = key in coffres

		if key_exist : 

			coffres.remove(key)
			with open(keyPath, 'w') as outfile:
				json.dump(coffres, outfile, indent=4)

	except : 
		pass

	return {"key_exist" : key_exist}