import random
import json

path = './keys.txt'

def New_Key():
	key = ""
	possible = list(range(48,58)) + list(range(65,91))
	for i in range(4):
		for j in range(4):
			key += chr(random.choice(possible))
		key += "~"
	return key[:-1]

def Add_Keys(n):
	try : 
		with open(path) as json_file:
			keys = json.load(json_file)	

			
	except : 
		keys = []

	for i in range(n):
		key = New_Key()
		print(key)
		keys.append(key)

	try :
		with open(path, 'w') as outfile:
			json.dump(keys, outfile, indent=4)
	except:
		pass

#Add_Keys(15)
