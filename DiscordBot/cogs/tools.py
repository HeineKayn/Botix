from datetime import datetime
import json
import os

def Update_json(file,content):
	path = "../web_data/{}".format(file)
	date_format = "%Y/%m/%d %H:%M:%S" 

	# crée les dossiers si ils existent pas
	try : 
		os.makedirs("/".join(path.split("/")[:-1]))
	except :
		pass

	new_content = {"time" : datetime.now().strftime(date_format), "content" : content}

	with open(path, 'w') as outfile:
		json.dump(new_content, outfile, indent=4)