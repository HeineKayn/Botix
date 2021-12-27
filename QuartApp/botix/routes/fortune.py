from quart import Blueprint, render_template, redirect, url_for
from quart_auth import *

import json
import random

fortuneBP = Blueprint('fortune', __name__)

@fortuneBP.route("/")
@login_required
async def fortune():

	try : 
		with open('./static/coffres.txt') as json_file:
			coffres = json.load(json_file)
	except : 
		coffres = []

	try : 
		with open('./static/keys.txt') as json_file:
			keys = json.load(json_file)
	except : 
		keys = []
		
	return await render_template('fortune.html',coffres=coffres,keys=keys)

@fortuneBP.route("/first-time")
@login_required
async def fortune_shuffle():
	try : 
		with open('./static/coffres.txt') as json_file:
			coffres = json.load(json_file)
			random.shuffle(coffres)

		with open('./static/coffres.txt', 'w') as outfile:
			json.dump(coffres, outfile, indent=4)
	except : 
		pass
	return redirect("/botix/fortune")

@fortuneBP.route('/fortune_open', methods=['POST'])
@login_required
async def fortune_open():
	id_coffre = await request.form
	id_coffre = int(id_coffre['id_coffre']) - 1

	try : 
		with open('./static/coffres.txt') as json_file:
			coffres = json.load(json_file)
			coffres[id_coffre]["open"] = True

		with open('./static/coffres.txt', 'w') as outfile:
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
		with open('./static/keys.txt') as json_file:
			coffres = json.load(json_file)

		key_exist = key in coffres

		if key_exist : 

			coffres.remove(key)
			with open('./static/keys.txt', 'w') as outfile:
				json.dump(coffres, outfile, indent=4)

	except : 
		pass

	return {"key_exist" : key_exist}