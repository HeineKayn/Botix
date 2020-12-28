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

champ_list_url = 'https://leagueoflegends.fandom.com/wiki/Champion'
champ_grid = Scrap(champ_list_url).find("div",{"id":"champion-grid"}) 
champ_list = champ_grid.findAll("a")

data = {}

for champ in champ_list :

	champ_link = champ["href"]
	champ_name = champ_link[6:]
	champ_url = "https://leagueoflegends.fandom.com" + champ_link + "/Quotes"

	champ_page_content = Scrap(champ_url).find("div",{"id":"mw-content-text"})

	data[champ_name] = {}

	for citation in champ_page_content.findAll("li") :

		try : 
			texte = citation.i.text
			audio = citation.button['onclick'].split(",")[2][12:]
		
			data[champ_name][texte] = audio

		except : 
			pass

with open('Audio_EN.txt','w') as outfile : 
	json.dump(data,outfile,indent=4)