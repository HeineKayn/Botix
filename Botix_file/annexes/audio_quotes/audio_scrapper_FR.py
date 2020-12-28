import asyncio
import os 

import requests

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

import json

# ====================

def Scrap(url):

	uClient = uReq(url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	return page_soup

# ====================

data = {}

champ_list_url = 'https://leagueoflegends.fandom.com/fr/wiki/Cat%C3%A9gorie:Champion'
champ_list = Scrap(champ_list_url).findAll("a",{"class":"category-page__member-link"})

for champ in champ_list :

	try : 

		champ_name = champ["title"].replace(" ","_")

		champ_url = "https://leagueoflegends.fandom.com/fr/" + champ_name + "/Historique"
		champ_page_content = Scrap(champ_url).find("div",{"id":"mw-content-text"})
		data[champ_name] = {}

		for citation in champ_page_content.findAll("li") :

			try : 
				texte = citation.i.text
				audio = citation.a["href"]
			
				data[champ_name][texte] = audio

			except : 
				pass

	except : 
		pass

with open('Audio_FR.txt','w') as outfile : 
	json.dump(data,outfile,indent=4)
