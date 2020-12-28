import discord
from discord.utils import get
from discord.ext import commands

from dotenv import load_dotenv
import os 

from discord.ext.ipc import Server
from datetime import datetime

# ---------------

import aiomysql
import sys
import os 
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_User')
password = os.getenv('DB_Password')
host = os.getenv('DB_Host')
port = int(os.getenv('DB_Port'))

# --------------

TOKEN = os.getenv('Test_Token')

intents = discord.Intents.all()

initial_extensions = [#'cogs.ipc',
					  'cogs.memo']

class Bot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	async def on_ready(self):
		await bot.change_presence(activity=discord.Game("se confiner"))

		print ("\n {} is connected to the following guild:\n".format(bot.user))
		for guild in bot.guilds:
			print(" {} : {} \n".format(guild.name,guild.id))

		self.conn = await aiomysql.connect(host=host, 
										   port=port,
										   user=user, 
										   password=password, 
										   db='memo')

		self.cur = await self.conn.cursor() 
		print("Connecté à la base de donnée")

		if __name__ == '__main__': # si le fichier est directement éxécuté et pas importé
			for extension in initial_extensions:
				bot.load_extension(extension)
	
	async def on_ipc_ready(self):
		print("Ipc ready.")


bot = Bot(command_prefix=['$','£'],intents=intents, description='Super Bot pouah',owner_id='174112128548995072')
bot_ipc = Server(bot, "localhost", 8765, "SALUT")

@bot_ipc.route()
async def get_last_messages(data):
	limit		 = data.limit
	server_name  = data.server		
	channel_name = data.channel

	guild   = discord.utils.get(bot.guilds, name = server_name)
	channel = discord.utils.get(guild.channels, name = channel_name)

	historique = []
	messages = await channel.history(limit=limit).flatten()
	for message in messages:
		histo_dic				= {}
		histo_dic["avatar"]		= str(message.author.avatar_url)
		histo_dic["name"]		= message.author.name
		histo_dic["content"]	= [message.clean_content]
		histo_dic["colour"]	 = str(message.author.colour)

		histo_dic["attachements"]			= []
		for attach in message.attachments :

			attach_dic 			= {}
			attach_dic["name"] 	= attach.filename
			attach_dic["url"] 	= attach.url
			histo_dic ["attachements"].append(attach_dic) 

		decal_today = (datetime.now() - message.created_at).days
		if decal_today == 0 :
			date = message.created_at.strftime("Aujourd'hui à %H:%M")
		elif decal_today == 1:
			date = message.created_at.strftime("Hier à %H:%M")
		elif decal_today == 2:
			date = message.created_at.strftime("Avant-hier à %H:%M")
		else :
			date = message.created_at.strftime("%d/%m/%Y")

		histo_dic["date"] = date
		historique.append(histo_dic)

	return historique

@bot_ipc.route()
async def get_demaciens(data):
	demaciens = []
	try : 
		server_name  = data.server 
		channel_name = data.channel  

		guild   = discord.utils.get(bot.guilds, name = server_name)
		channel = discord.utils.get(guild.channels, name = channel_name)
		role = discord.utils.get(guild.roles, name = "Demacien")

		members = [x for x in channel.members if role in x.roles]
		for member in members:

			demacien_dic			= {}
			demacien_dic["avatar"]	= str(member.avatar_url)
			demacien_dic["name"]	= member.name
			demacien_dic["name_id"]	= "{} - {}".format(member.name,member.id)
			demaciens.append(demacien_dic)
	except : 
		pass

	return demaciens

@bot_ipc.route()
async def get_onlines(data):
	server_name  = data.server 
	channel_name = data.channel  

	maisons = ["Vayne","Buvelle","Crownguard","Laurent","Cloudfield"]
	guild   = discord.utils.get(bot.guilds, name = server_name)
	channel = discord.utils.get(guild.channels, name = channel_name)
	role = discord.utils.get(guild.roles, name = "Demacien")

	onlines = {}

	members = [x for x in channel.members if role in x.roles]
	for member in members:

		if member.raw_status != "offline" :
			online_dic				= {}
			online_dic["avatar"]	= str(member.avatar_url)
			online_dic["name"]		= member.name
			online_dic["status"]	= member.raw_status
			online_dic["colour"]	= str(member.colour)

			try :
				maison  = [str(x) for x in member.roles if str(x) in maisons][0]
			except :
				maison = "Demacien"

			if maison in onlines:
				onlines[maison] += [online_dic]
			else : 
				onlines[maison] = [online_dic]

	return onlines

@bot_ipc.route()
async def get_servers_name(data):
	guild_infos = []
	for guild in bot.guilds :
		guild_dic		 = {}
		guild_dic["icon"] = str(guild.icon_url)
		guild_dic["name"] = guild.name
		guild_infos.append(guild_dic)
	return guild_infos

@bot_ipc.route()
async def get_channels_name(data):
	server_name  = data.server		# "The Kingdom Of Demacia"
	guild   = discord.utils.get(bot.guilds, name = server_name)

	channels = []
	for channel in guild.text_channels : 
		channels.append(channel.name)
	return channels

@bot_ipc.route()
async def get_memos(data):
	uid = data.user_id
	author_tagged = "<@!" + str(uid) + ">"
	author_roles = []
	for guild in bot.guilds : 
		try : 
			author = await guild.get_member(uid)
			author_roles += ["<@&"+str(x.id)+">" for x in author.roles]
		except:
			pass

	concerne = author_roles + [author_tagged]

	Q_Memo = """
				SELECT 
					DATE_FORMAT(DateCreated,%s), 
					DATE_FORMAT(DatePlanned,%s), 
					idGuild, idChannel, idInvoker, Content, idMessage
				FROM Horaire 
				INNER JOIN Info
				ON Horaire.ID = Info.idHoraire
				WHERE 
					idInvoker = (%s) OR 
					{}
				ORDER BY DatePlanned ASC
			 """

	Format_LIKE = "Content LIKE '%%{}%%'"
	concerne = [Format_LIKE.format(x) for x in concerne]
	concerne = " OR ".join(concerne)
	Q_Memo = Q_Memo.format(concerne)

	DBUser = "%Y/%m/%d à %H:%i"
	await bot.cur.execute(Q_Memo,(DBUser,DBUser,uid,)) # peut être add virgule après
	query_result = await bot.cur.fetchall()

	list_memos = []
	for result in query_result : 
		(DateCreated, DatePlanned, idGuild, idChannel, idInvoker, Content, idMessage) = result
		guild = discord.utils.get(bot.guilds, id = idGuild)
		channel = discord.utils.get(guild.channels, id = idChannel)

		try :
			invoker = await bot.fetch_user(idInvoker)
			invoker_dic = {"name" : invoker.name, "avatar" : str(invoker.avatar_url)}
		except:
			invoker_name = "?" 
			invoker_pp = "https://cdn.discordapp.com/embed/avatars/0.png"

		invoked = await bot.fetch_user(uid)
		invoked_dic = {"name" : invoked.name, "avatar" : str(invoked.avatar_url)}

		memo_dic = {"created" : DateCreated, "planned" : DatePlanned, "guild" : guild.name, "channel" : channel.name, 
					"invoker" : invoker_dic, "invoked" : invoked_dic, "content" : Content, "idMessage" : idMessage}

		list_memos.append(memo_dic)
	return list_memos

### ----------------------------------

if __name__ == "__main__":
	bot_ipc.start()
	bot.run(TOKEN,bot=True)
	

# print(os.getcwd())