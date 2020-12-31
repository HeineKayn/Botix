from quart import Quart, render_template, redirect, url_for
from discord.ext.ipc import Client
from datetime import datetime 

import json
import random

app = Quart(__name__)
web_ipc = Client(secret_key="SALUT")

# ---------------

from quart_auth import *

auth_manager = AuthManager(app)
app.secret_key = "secret key"  # Do not use this key
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
				# if await current_user.is_authenticated :
				# 	login_user()
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

@app.route("/")
@app.route("/place_publique")
@app.route("/place_publique/<channel>")
async def place_publique(channel=""):

	guild = "bdo"
	if channel not in ["a","général","solo","post-it"] : # ["🏰place_publique"]
		channel = "général"

	## TEST ##
	# guild = "Botix Showcase"

	messages = await last_messages(guild,channel,100)  # "The Kingdom Of Demacia","🏰place_publique"
	messages = eval(messages)

	# onlines = await online_list(guild,channel)
	# onlines = eval(onlines)
	demaciens = await app.ipc_node.request("get_demaciens",server = guild, channel = channel)

	return await render_template('place_publique.html',messages=messages, demacien_list=demaciens)

@app.route("/memo")
@app.route("/memo/<id_user>")
async def memo(id_user=0):
	channel_name = "🏰place_publique"
	server_list = await app.ipc_node.request("get_servers_name")
	demaciens = []

	for server in server_list :
		try : 
			server_name = server["name"]
			demaciens += await app.ipc_node.request("get_demaciens", server = server_name, channel = channel_name)
		except :
			pass

	demaciens = [i for n, i in enumerate(demaciens) if i not in demaciens[n + 1:]]

	id_user = int(id_user)
	memos = []
	if id_user :
		memos = await app.ipc_node.request("get_memos", user_id=id_user)
	return await render_template('memo.html',demacien_list=demaciens,memos=memos)

@app.route("/memo/<id_user>/<id_message>")
async def memo_delete(id_user,id_message):
	# await app.ipc_node.request("remove_memo",id_message=id_message)
	return redirect(url_for('memo',id_user=id_user))

@app.route("/fortune")
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

@app.route("/fortune/<id_coffre>")
async def fortune_open(id_coffre):

	id_coffre = int(id_coffre) - 1

	try : 
		with open('./static/coffres.txt') as json_file:
			coffres = json.load(json_file)
			coffres[id_coffre]["open"] = True

		with open('./static/coffres.txt', 'w') as outfile:
   			json.dump(coffres, outfile, indent=4)
	except : 
		pass

	return redirect(url_for('fortune'))

@app.route("/fortune-first-time")
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

@app.route("/api")
async def api():
	return """
			<p><a href="last_mess">Last Messages</a></p>
			<p><a href="online">Online</a></p>
			<p><a href="guilds">Servers</a></p>
			<p><a href="channels">Channels</a></p>
		   """

@app.route("/online")
async def online_list(server_name = "bdo", channel_name = "général"):
	onlines = await app.ipc_node.request("get_onlines", server = server_name, channel = channel_name)
	return str(onlines)

@app.route("/guilds")
async def guild_list():
	guilds = await app.ipc_node.request("get_servers_name")
	return str(guilds)

@app.route("/channels")
async def channel_list(server_name = "bdo"):
	channels = await app.ipc_node.request("get_channels_name", server = server_name)
	return str(channels)

@app.route("/last_mess")
async def last_messages(server_name = "bdo", channel_name = "général", limit = 20):
	messages = await app.ipc_node.request("get_last_messages", server = server_name, channel = channel_name, limit = limit)
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

	return str(messages)

# ---------------

@app.before_first_request
async def before():
	app.ipc_node = await web_ipc.discover() 

if __name__ == "__main__":
	app.run()