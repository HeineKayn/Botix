import json

coffres = {}

coffres[1] = ["huitre","poulet","dinde"]
coffres[2] = ["a","b","c"]


with open('password.txt', 'w') as outfile:
    json.dump(coffres, outfile, indent=4)