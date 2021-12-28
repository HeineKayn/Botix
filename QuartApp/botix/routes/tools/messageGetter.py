from .tools import *

async def get_last_messages(app,guild="bdo",channel="général",limit=100):
    file = "messages/{}/{}.txt".format(guild,channel)
    delay = 5

    if Need_update(file,delay):
        await app.request("get_last_messages",server=guild,channel=channel,limit=limit)

    messages = Get_json(file)
    messages.reverse()
    id_redondants = []

    for i,message in enumerate(messages): # Si la même personne a envoyé 2 messages successif le même jour

        if i > 0 :
            meme_nom = messages[i]['name'] == messages[i-1]['name'] 

            if meme_nom :
                hier_ou_ajd = not messages[i]['date'][0].isdigit()

                if hier_ou_ajd : 
                    meme_jour = messages[i]['date'].split()[0] == messages[i-1]['date'].split()[0]

                    if meme_jour :
                        laps_minute  = (datetime.strptime(messages[i]['date'].split()[2],"%H:%M").minute - datetime.strptime(messages[i-1]['date'].split()[2],"%H:%M").minute)

                        if laps_minute < 10 : 
                            id_redondants.append(i)

                elif messages[i]['date'] == messages[i-1]['date'] :
                    id_redondants.append(i)

    id_redondants.reverse()
    for i in id_redondants :
        messages[i-1]["content"] += messages[i]["content"]
        messages[i-1]["attachements"] += messages[i]["attachements"]

    for i in id_redondants : 
        messages.pop(i)

    return messages