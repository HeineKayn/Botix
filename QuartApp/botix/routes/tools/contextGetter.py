from .tools import *

async def get_demaciens(app,guild="bdo",channel="général"):
	file = "demaciens/{}/{}.txt".format(guild,channel)
	delay = 10

	if Need_update(file,delay):
		await app.request("get_demaciens",server = guild, channel = channel)
	return Get_json(file)

async def get_guilds(app):
	file = "guilds.txt"
	delay = 60

	if Need_update(file,delay):
		await app.request("get_guilds")
	return Get_json(file)

async def get_channels(app,guild="bdo"):
	file = "guilds/{}.txt".format(guild)
	delay = 60

	if Need_update(file,delay):
		await app.request("get_channels", server = guild)
	return Get_json(file)