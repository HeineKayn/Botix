from datetime import datetime
import json

def Need_update(file,delay=1):
	path = "./web_data/{}".format(file)
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
	path = "./web_data/{}".format(file)

	with open(path) as json_file:
		data = json.load(json_file)["content"]

	return data