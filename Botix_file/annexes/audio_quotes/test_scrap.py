from urllib.request import urlopen as uReq
from PIL import Image
from bs4 import BeautifulSoup as soup

url = 'http://demacia.fr/'

uClient = uReq(url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

# ==================

containers_maisons = page_soup.findAll("div",{"class":"col-sm-12"})

buvelle = containers_maisons[0]
buvelle_name = buvelle.p.span.strong.text.strip()
buvelle_liste = buvelle.findAll("a",{"class":buvelle_name.lower()})

for maison in containers_maisons :

	if maison["class"] == ['col-sm-12'] :

		try : 
			maison_name = maison.p.span.strong.text.strip()
			maison_liste = maison.findAll("a",{"class": maison_name.lower()})
			maison_liste += maison.findAll("a",{"class": "chatelain"})

			print("================ " + maison_name + " ================")

			for demacien in maison_liste :
				pic = "http://demacia.fr" + demacien.img["src"].strip()
				name = demacien.text.strip()
				print(name)

				######

				im = Image.open(uReq(pic))
				im.show()
				break
		except : 
			pass
	break
