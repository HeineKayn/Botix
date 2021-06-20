from quart import Quart, render_template, redirect, url_for
from discord.ext.ipc import Client
from datetime import datetime 

import os
import json
import random

# ---------------

from dotenv import load_dotenv

load_dotenv()
ipc_pass = os.getenv('IPC_Pass')
app_pass = os.getenv('APP_Pass')

# ---------------

app = Quart(__name__)
web_ipc = Client(secret_key=ipc_pass)

# ---------------

from quart_auth import *

auth_manager = AuthManager(app)
app.secret_key = app_pass  # Do not use this key
app.config.from_mapping(QUART_AUTH_COOKIE_HTTP_ONLY=False)
app.config.from_mapping(QUART_AUTH_COOKIE_SECURE=False)
app.config.from_mapping(QUART_AUTH_COOKIE_SECURE=False)

# ---------------

@app.route("/login")
async def login(password=""):
	if not current_user.auth_id :
		return await render_template('login.html')
	else : 
		logout_user()
		return redirect("/")

@app.route("/login/<password>")
async def login_mdp(password=""):
	if password != "" :
		try : 
			with open('./static/password.txt') as json_file:
				mdp_dic = json.load(json_file)
		except : 
			mdp_dic = []

		for key, mdp_list in mdp_dic.items():
			if password in mdp_list :
				login_user(user=AuthUser(int(key)),remember=True)

	if not current_user.auth_id :
		return redirect(url_for('login'))
	else : 
		return redirect("/")

@app.route("/logout")
async def logout():
	logout_user()
	return redirect("/")
	
@app.route("/restrict")
@login_required
async def restricted_route():
	print(current_user.auth_id) # Will be 2 given the login_user code above
	return "Non connecté"

# ---------------

from datetime import datetime
import json

def Need_update(file,delay=1):
	path = "../web_data/{}".format(file)
	date_format = "%Y/%m/%d %H:%M:%S" 
	now = datetime.now()

	try : 
		with open(path) as json_file:
			content = json.load(json_file)
			old_date = datetime.strptime(content["time"],date_format)

	except : 
		old_date = None

	return not old_date or (now - old_date).total_seconds() > delay

def Get_json(file):
	path = "../web_data/{}".format(file)

	with open(path) as json_file:
		data = json.load(json_file)["content"]

	return data

# ---------------

async def get_demaciens(guild="bdo",channel="général"):
	file = "demaciens/{}/{}.txt".format(guild,channel)
	delay = 10

	if Need_update(file,delay):
		await app.ipc_node.request("get_demaciens",server = guild, channel = channel)
	return Get_json(file)

async def get_guilds():
	file = "guilds.txt"
	delay = 60

	if Need_update(file,delay):
		await app.ipc_node.request("get_guilds")
	return Get_json(file)

async def get_channels(guild="bdo"):
	file = "guilds/{}.txt".format(guild)
	delay = 60

	if Need_update(file,delay):
		await app.ipc_node.request("get_channels", server = guild)
	return Get_json(file)

async def get_memos(user_id=174112128548995072):
	file = "memos/{}.txt".format(str(user_id))
	delay = 1

	if Need_update(file,delay):
		await app.ipc_node.request("get_memos", user_id = user_id)
	return Get_json(file)

async def get_last_messages(guild="bdo",channel="général",limit=100):
	file = "messages/{}/{}.txt".format(guild,channel)
	delay = 5

	if Need_update(file,delay):
		await app.ipc_node.request("get_last_messages",server=guild,channel=channel,limit=limit)

	messages = Get_json(file)
	messages.reverse()
	id_redondants = []

	for i,message in enumerate(messages): # Si la même personne a envoyé 2 messages successif le même jour

		if i > 0 :
			meme_nom = messages[i]['name'] == messages[i-1]['name'] 

			if meme_nom :
				hier_ou_ajd = not messages[i]['date'][0].isdigit()

				if hier_ou_ajd : 
					meme_jour = messages[i]['date'].split()[0] == messages[i-1]['date'].split()[0]

					if meme_jour :
						laps_minute  = (datetime.strptime(messages[i]['date'].split()[2],"%H:%M").minute - datetime.strptime(messages[i-1]['date'].split()[2],"%H:%M").minute)

						if laps_minute < 10 : 
							id_redondants.append(i)

				elif messages[i]['date'] == messages[i-1]['date'] :
					id_redondants.append(i)

	id_redondants.reverse()
	for i in id_redondants :
		messages[i-1]["content"] += messages[i]["content"]
		messages[i-1]["attachements"] += messages[i]["attachements"]

	for i in id_redondants : 
		messages.pop(i)

	return messages

async def get_bombes():
	path = "../Botix_file/annexes/musiques"
	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
	files = [f.split(".mp3")[0] for f in files]
	return files

# ---------------

@app.route("/")
@app.route("/place_publique")
@app.route("/place_publique/<channel>")
async def place_publique(channel=""):

	guild = "bdo" # "The Kingdom Of Demacia"
	channel = "général" # "🏰place_publique"

	messages = await get_last_messages(guild,channel,100)
	demaciens = await get_demaciens(guild,channel)

	return await render_template('place_publique.html',messages=messages, demacien_list=demaciens)

@app.route("/memo")
@app.route("/memo/<id_user>")
@login_required
async def memo(id_user="0"):
	channel = "🏰place_publique"
	server_list = await get_guilds()
	demaciens = {}
	server_demaciens = {}

	for server in server_list :
		try : 
			server_name = server["name"]
			server_demaciens = await get_demaciens(server_name,channel)
			for key,val in server_demaciens.items():

				if key in demaciens :
					demaciens[key] += server_demaciens[key]
				else :
					demaciens[key] = server_demaciens[key]
		except :
			pass
	
	for key_1,val_1 in demaciens.items():

		# élimine les redondances dans la même maisons
		demaciens[key_1] = [i for n, i in enumerate(demaciens[key_1]) if i["name"] not in [x["name"] for x in demaciens[key_1]][n + 1:]]

		# élimine les redondances entre les maisons
		for key_2,val_2 in demaciens.items():
			if key_1 != key_2 : 
				demaciens[key_1] = [x for x in demaciens[key_1] if x["name"] not in [y["name"] for y in demaciens[key_2]]]

	id_user = int(id_user)
	memos = []
	if id_user :
		memos = await get_memos(id_user)
	return await render_template('memo.html',demacien_list=demaciens,memos=memos)

@app.route("/memo/<id_user>/<id_message>")
@login_required
async def memo_delete(id_user,id_message):
	await app.ipc_node.request("remove_memo",id_message=id_message)
	return redirect(url_for('memo',id_user=id_user))

@app.route("/fortune")
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

@app.route("/fortune-first-time")
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
	return redirect(url_for('fortune'))

@app.route('/fortune_open', methods=['POST'])
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

@app.route('/use_key', methods=['POST'])
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

@app.route("/config")
@login_required
async def config():
	config = await app.ipc_node.request("get_config")
	return await render_template('config.html',config=config)

@app.route("/config_element", methods=['POST'])
@login_required
async def config_element():
	req = await request.form
	dic = {req["name"] : req["value"]}
	await app.ipc_node.request("set_config",config=dic)
	return {}

import random

@app.route("/generate_key", methods=['POST'])
@login_required
async def generate_key():
	req = await request.form
	nb = int(req["number"])
	path = './static/keys.txt'

	try : 
		with open(path) as json_file:
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
		with open(path, 'w') as outfile:
			json.dump(keys, outfile, indent=4)
	except:
		pass

	return {"generated" : nb}

@app.route("/communiquer")
@login_required
async def communiquer():
	guild_list = await get_guilds()
	return await render_template('communiquer.html',guild_list=guild_list)

# @app.route("/communiquer")
# @app.route("/communiquer/<guild>/<channel>")
# @login_required
# async def communiquer(guild="",channel=""):
# 	guild_list = await get_guilds()

# 	if channel != "":
# 		messages = await get_last_messages(guild,channel,100)
# 	else :
# 		messages = []

# 	return await render_template('communiquer.html',guild_list=guild_list,guild=guild,channel=channel,messages=messages)

@app.route("/select_guild", methods=['POST'])
@login_required
async def select_guild():
	req = await request.form
	selected_guild = req["guild"]
	guild_list = await get_guilds()
	channel_list = []
	for guild in guild_list :
		if selected_guild == guild["name"]:
			channel_list = await get_channels(selected_guild)
			break
	return {"channel_list" : channel_list}

@app.route("/select_channel", methods=['POST'])
@login_required
async def select_channel():
	req = await request.form
	guild = req["guild"]
	channel = req["channel"]
	messages = await get_last_messages(guild,channel,100)
	return {"messages" : messages}

@app.route("/send_message", methods=['POST'])
@login_required
async def send_message():
	req = await request.form
	await app.ipc_node.request("send_message",guild=req["guild"],channel=req["channel"],message=req["content"])
	return {}

@app.route("/musique")
@login_required
async def musique():
	guild_list = await get_guilds()
	bombes = await get_bombes()
	return await render_template('musique.html',serveurs=guild_list,bombes=bombes)

@app.route("/logs")
@login_required
async def logs():
	return await render_template('logs.html')

# ---------------

@app.before_first_request
async def before():
	app.ipc_node = await web_ipc.discover() 

if __name__ == "__main__":
	app.run()