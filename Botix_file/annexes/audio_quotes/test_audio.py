import requests

url = "https://vignette.wikia.nocookie.net/leagueoflegends/images/0/04/Vi.move1.ogg/revision/latest?cb=20121208081727"
r = requests.get(url, allow_redirects=True)

open('vi.mp3', 'wb').write(r.content)