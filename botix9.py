import os
import random
import datetime
import asyncio
import typing
import discord
import youtube_dl

from ub_display import DisplayUB
from limite_limite2 import *

from discord.utils import get
from discord import FFmpegPCMAudio

from discord.ext import commands
from dotenv import load_dotenv

import email
import imaplib
from email import policy

from operator import attrgetter
from waiting import wait, TimeoutExpired

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$',description='Super Bot pouah',owner_id='174112128548995072')

# ------------------------ Definitions ------------------------

espion = ["deltix","luxanna","buvelle"]

with open("./ban.txt", "r", encoding="utf-8", errors ="ignore") as bantxt:
        banread = bantxt.read()
banlist = banread.split("\n")

with open("./banword.txt", "r", encoding="utf-8", errors ="ignore") as banwordtxt:
        banwordread = banwordtxt.read()
banwordlist = banwordread.split("\n")


liens = {
    "site" : "http://demacia.fr/",
    "serment" : "https://docs.google.com/document/d/1-Yk4mgFttjCQMIctKLq8U_B4r8jLBF8M8mN085Nnrs0/edit?usp=sharing",
    "maisons" : "https://docs.google.com/document/d/19EB6HEkQ0utrKXC_sE2w6NEQtmTfk23I4fWAoZYL3P0/edit?usp=sharing",
    "guide" : "https://docs.google.com/document/d/1OOC4xFVGvMgZLhCNgHRqwvk8WsC6n_iHhL-ajC6gwpA/edit?usp=sharing",
    "mundo" : "https://docs.google.com/document/d/1GnjVhMfKWWyjOFq6wg1nNQigAL7j-T_xEGEUv1WF8Ds/edit?usp=sharing",
    "sketch" : "https://docs.google.com/document/d/1CoK23txxQY4cCrq7qObg3nCb22GWw92kHLYT0lMVHjU/edit?usp=sharing",
    "tokor" : "https://drive.google.com/file/d/1isKoEpFKycOmrjjHRQ1t4mKSyzldXBPr/view?usp=sharing",
    "asheraly" : "https://drive.google.com/file/d/1zrNfJtTJejgfRaUUmujraIVdrWUvTm9c/view?usp=sharing",
    "charon" : "https://drive.google.com/file/d/14N9gCs7Trq3HdkMBAVmNcLnvYoB8QbQt/view?usp=sharing",
    "lunny" : "https://drive.google.com/file/d/166GzZIb1ANuP8LFbzECkz4nFANBoIS2W/view?usp=sharing",
    "ouria" : "https://drive.google.com/file/d/1UarjNgOrcSd_fMHZTNjWX4NeejXJRCEs/view?usp=sharing",
 }

def isowner(ctx):
    return ctx.message.author.id == 174112128548995072

def noban(ctx):
    return ctx.message.author.id not in banlist

# ------------------------ Core ------------------------

# -------------- Admin

@bot.event # Montre dans Console qu'il est co et où
async def on_ready():
    await bot.change_presence(activity=discord.Game("se confiner"))
    print ("\n {} is connected to the following guild:\n".format(bot.user))
    for guild in bot.guilds:
        print(" {} : {} \n".format(guild.name,guild.id))

# @bot.event
# async def on_member_join(member):
#     await member.send('Bienvenue dans Demacia')

# @bot.event
# async def on_message(message): # si les mots de espion sont prononcés la phrase est stocké dans un fichier log
#     # esp = [i for i in espion if i in message.content.lower()]
#     # if len(esp) > 0 and isinstance(message.channel,discord.TextChannel):
#     #     with open("./log.txt", "a", encoding="utf-8", errors ="ignore") as log:
#     #         log.write("{0} -> {1} in {2} de {3} : {4}\n".format(datetime.datetime.now(),message.author,message.channel.name,message.guild.name,message.content))
#     bword = [i for i in banwordlist if i in message.content.lower()]
#     if len(bword) > 0 and isinstance(message.channel,discord.TextChannel):
#         allroles = message.author.roles
#         if len(allroles) > 1:
#             del allroles[0]
#             for i in allroles:
#                 await message.author.remove_roles(i)
#             await message.channel.send("Tous les rôles de {} ont été supprimés pour avoir dit ({}).\nPour toute réclamation mp Temari".format(message.author,', '.join(bword)))
#     await bot.process_commands(message)

# @bot.command(name='shutdown',aliases=['ciao','bye','adieu','sleep'],hidden=True) # Deco si je demande
# @commands.check(isowner)
# async def shutdown(ctx):
#     sleep = ['Zzzzz je m\'endors','Nooooooo... :skull:','Adieu monde cruel', 'Je vais me reposer uwu']
#     rsleep = random.choice(sleep)
#     await ctx.send(rsleep)
#     await bot.close()

# @bot.command(name='clear',aliases=['purge','vide'],hidden=True) # Clear n messages
# @commands.check(isowner)
# async def clear(ctx, nombre = 1):
# 	await ctx.channel.purge(limit = nombre + 1)

# @bot.command(name='banlistadd',aliases=['addb','addban'],hidden=True) # Ajoute member à la ban list
# @commands.check(isowner)
# async def banlistadd(ctx, member : int):
#     if member not in banlist:
#         banlist.append(str(member))
#         with open("./ban.txt", "a", encoding="utf-8", errors ="ignore") as bantxt:
#             bantxt.write(str(member) + "\n")

# @bot.command(name='banlistrm',aliases=['rmb','rmban'],hidden=True) # Enleve member à la ban list
# @commands.check(isowner)
# async def banlistrm(ctx, member : int):
#     if str(member) in banlist:
#         banlist[banlist.index(str(member))] = ""
#         bantxt = open("ban.txt", "w") 
#         with open("./ban.txt", "a", encoding="utf-8", errors ="ignore") as bantxt:
#             for ban in banlist:
#                 if ban != "":
#                     bantxt.write(str(ban) + "\n") 

# @bot.command(name='getbanlist',aliases=['lban','banl'],hidden=True) # Donne la banlist
# @commands.check(isowner)
# async def getbanlist(ctx):
# 	blist = [int(x) for x in banlist if x != ""]
# 	e = []
# 	if len(blist) > 0:
# 		for i in blist:
# 			e.append(str(ctx.guild.get_member(i)))
# 		await ctx.send('Utilisateurs qui ne peuvent pas utiliser le bot :\n{}'.format(', '.join(e)))
# 	else:
# 		await ctx.send("Personne n'est ban uwu")

selected = None

@bot.command(name='select',aliases=['sel','choose'],hidden=True) # Donne la banlist
@commands.check(isowner)
async def select(ctx,guildname,channelname):
    global selected
    guild = discord.utils.get(bot.guilds, name=guildname)
    selected = discord.utils.get(guild.channels, name=channelname) 

@bot.command(name='botsay',aliases=['puppet','bsay'],hidden=True) # Donne la banlist
@commands.check(isowner)
async def botsay(ctx,*args):
    try:
        await selected.send(' '.join(args))
    except:
        await ctx.send("Aucun channel selectionné")

@bot.command(name='botdm',hidden=True)
@commands.check(isowner)
async def botdm(ctx,member: discord.Member,*args):
    await member.send(' '.join(args))

@bot.command(name='type',aliases=['ty','fake'],hidden=True) # Donne la banlist
@commands.check(isowner)
async def type(ctx,time=10):
    async with selected.typing():
       await asyncio.sleep(time)
    # await selected.trigger_typing()

# async def AlwaysType():
#     await bot.wait_until_ready()
#     pause = 3
#     while not bot.is_closed():
#         if selected != None:
#             categorie = selected.category
#             channel = random.choice(categorie.text_channels)
#             await channel.trigger_typing()
#             print("Le bot est entrain d'écrire dans le channel :" + channel.name)
#             pause = random.randint(5,100)
#             print("Attente de : {} secondes ".format(pause))
#         await asyncio.sleep(pause)

# bot.loop.create_task(AlwaysType())

# -------------- Utile 

@bot.command(name='doc',aliases=['lien','liens','docs'],hidden=True)
@commands.check(isowner)
async def doc(ctx,key):
    key = key.lower()
    if key == "help" or "":
        await ctx.send("Documents : {}".format(', '.join(liens.keys())))
    elif key in liens.keys():
        await ctx.send(liens[key])
    else:
        await ctx.send("Ce document n'existe pas :/")

File_Memo = []

class TypeMemo:
    def __init__(self,time,ctx,args):
        self.time = time
        self.ctx = ctx
        self.args = args
    def new_time(self, time2): 
        self.time = tim2

def CroissFile(file,memo,cache=[]):
    if len(file) == 0 or memo.time > file[-1].time:
        file.append(memo)
        file2 = file + cache
    else:
        pop = []
        pop.append(file[-1])
        file2 = CroissFile(file[:-1],memo,pop+cache)
    return file2

def EqualTimes(t1,t2):
    return t1.strftime("%d/%m/%Y à %H:%M") == t2.strftime("%d/%m/%Y à %H:%M") and abs(int(t1.strftime("%S")) - int(t2.strftime("%S"))) < 4

def HowManyIn(file,memo):
    n = 0
    if len(file) > 0:
        for i in file:
            if EqualTimes(i.time,memo.time):
                n += 1
    return n

@bot.command(name='rappel',aliases=['remindme','memo','remind'],help="-> Notifie un certains temps plus tard",hidden=True) # Rappelle un truc à une certaine date
async def rappel(ctx, secondes: typing.Optional[int] = 0, minutes: typing.Optional[int] = 0, heures: typing.Optional[int] = 0, jours: typing.Optional[int] = 0, *args):
    global File_Memo
    heures = min(24,heures)
    minutes = min(60,minutes)
    secondes = min(60,secondes)
    secondes = max(1,secondes)
    decal = datetime.datetime.now() + datetime.timedelta(seconds=secondes,minutes=minutes,hours=heures,days=jours) 
    memo = TypeMemo(decal,ctx,args)
    File_Memo = CroissFile(File_Memo,memo)
    await ctx.send("Rappel enregistré. \nJe te notifierais le " + decal.strftime("%d/%m/%Y à %H:%M:%S"))

async def MemoBackGround():
    await bot.wait_until_ready()
    while not bot.is_closed():
        global File_Memo
        if len(File_Memo) > 0 and EqualTimes(File_Memo[0].time,datetime.datetime.now()):
            count = HowManyIn(File_Memo,File_Memo[0])
            for i in range(count):
                ctx = File_Memo[0].ctx
                member = ctx.message.author
                args = File_Memo[0].args
                File_Memo.pop(0)
                await ctx.send("{} C'EST L'HEURE DE {}".format(member.mention,' '.join(args)))
        await asyncio.sleep(1)

bot.loop.create_task(MemoBackGround())

@bot.command(name='action',hidden=True)
@commands.check(isowner)
async def action(ctx,member: discord.Member,*args):
	await ctx.send('{0} {2} {1}'.format(ctx.message.author.mention,member.mention,' '.join(args)))

@bot.command(name='dm',hidden=True)
@commands.check(isowner)
async def dm(ctx,member: discord.Member,*args):
	await member.send('{0} te {1}'.format(ctx.message.author,' '.join(args)))

@bot.command(name='ping',hidden=True)
@commands.check(isowner)
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    await ctx.send(f"my ping is {ping}ms")

# -------------- Reaction à des messages


# -------------- Jeux

################################################## 

@bot.command(name='lstart',hidden=True)
@commands.check(isowner)
async def lstart(ctx):
    guild = discord.utils.get(bot.guilds, name="Limite Limite Demacien")
    channel = discord.utils.get(guild.channels, name="participer") 
    await guild.create_role(name="Participe")
    await channel.set_permissions(guild.default_role, view_channel = True, send_messages = False)

@bot.command(name='lstop',hidden=True)
@commands.check(isowner)
async def lstop(ctx):
    guild = discord.utils.get(bot.guilds, name="Limite Limite Demacien")
    channel = discord.utils.get(guild.channels, name="participer") 
    role = discord.utils.get(guild.roles,name="Participe")
    await role.delete()
    await channel.set_permissions(guild.default_role, view_channel = False)

async def React_Role(payload,adding):
    guild = discord.utils.get(bot.guilds, name="Limite Limite Demacien")
    channel = discord.utils.get(guild.channels, name="participer") 
    original_post = channel.last_message_id

    user_id = payload.user_id
    reacted_message_id = payload.message_id
    emoji = payload.emoji

    member = guild.get_member(user_id)
    if reacted_message_id == original_post and str(emoji) == "👍":
        role = discord.utils.get(guild.roles,name="Participe")
        if adding:
            await member.add_roles(role)
        if not adding:
            await member.remove_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    await React_Role(payload,True)
            
@bot.event
async def on_raw_reaction_remove(payload):
    await React_Role(payload,False)

@bot.command(name='limite',aliases=['lim','limitelimite','event_limite'], help='-> Limite Limite Demacien',hidden=True) # Ultimate Bravery
@commands.check(isowner)
async def limite(ctx,categorie ="soft",nbtour = 5):

######################### Remontre les cartes que le joueur a puis lui fait choisir celle qu'il veut jouer

    async def AttendsRep(Joueur,nbprop,nbneed,Partie,chef=False): # UTILISER LE PRINCIPE DE MEMO AVEC UNE FILE D'ATTENTE ET CA CHECK A CHAQUE FOIS SI IL A REP

        def dansRep(Partie,numbers):
            notFound = True
            for i in range(len(numbers)):
                if int(numbers[i]) > len(Partie.choicesGive):
                    notFound = False
            return notFound

        def dansMain(Joueur,numbers):
            notFound = True
            for i in range(len(numbers)):
                if int(numbers[i]) > len(Joueur.main):
                    notFound = False
            return notFound

        def double(string):
            found = False
            for i in range(len(string)):
                if string.count(string[i]) > 1:
                    found = True
            return found

        def check(m):
            if not m.guild and m.author == Joueur.name:
                a = ''.join(x for x in m.content if x.isdecimal() or x == " ")
                b = a.split()
                if chef :
                    return len(b) == nbneed and not double(b) and dansRep(Partie,b)
                else : 
                    return len(b) == nbneed and not double(b) and dansMain(Joueur,b)
            else:
                return False

        try:   
            number = await bot.wait_for('message', timeout=timer, check=check) # Attention si le message de la personne est pas valide ça s'affiche
            await Joueur.name.send("Votre réponse a bien été entregistrée")
            number = ''.join(x for x in number.content if x.isdecimal() or x == " ")
            numbers = number.split()
            for i in range(len(numbers)):
                numbers[i] = int(numbers[i])
        except asyncio.TimeoutError:
            await Joueur.name.send("Temps écoulé, une réponse aléatoire a été choisie")
            nblist = []
            numbers = []
            for i in range(1,nbprop):
                if Joueur.main[i-1] != "**JOKER**" :
                    nblist.append(i)
            for i in range(nbneed):
                r = random.choice(nblist)
                numbers.append(r)
                nblist.remove(r)
        return numbers

######################### 

    async def ChoixGive(Partie,Joueur):
        joker = None

        def checkJoker(m):
            return not m.guild and m.author == Joueur.name

        nbneed = Partie.question.trous
        lignes = []
        count = 1
        for carte in Joueur.main:
            lignes.append("{} - {}".format(count,carte))
            count += 1

        await Joueur.name.send("Tiens, {} , voici un rappel de la phrase à compléter (Attention vous n'avez que {} secondes): \n- `{}`\n\nVoici ta main : \n{} \nRéponds en envoyant ici les numéros des **{}** réponses que tu préfères séparées par des espaces".format(Joueur.name.name,timer,Partie.question.carte,'\n'.join(lignes),nbneed)) 

        reponses = await AttendsRep(Joueur,count,nbneed,Partie,False)

        for i in range(len(reponses)):
            reponses[i] = Joueur.main[reponses[i]-1]
            if reponses[i] == "**JOKER**":
                await Joueur.name.send("Ecrivez votre Joker")
                try :
                    joker = await bot.wait_for('message', timeout=timer, check=checkJoker) 
                    joker = joker.content
                except : 
                    joker = "Joker par défaut"
                await Joueur.name.send("Votre réponse a bien été entregistrée")
                reponses[i] = joker

        decision = Choice(reponses,Joueur)
        Joueur.pick = decision
        for i in decision.choices:
            if i == joker:
                Joueur.main.remove("**JOKER**")
                Partie.pileR.defausse.append("**JOKER**")
            else:
                Joueur.main.remove(i)
                Partie.pileR.defausse.append(i)
            pioche(Joueur,Partie.pileR)

######################### 

    async def ChoixTake(Partie):
        Joueur = Partie.lead
        lignes = []
        count = 1
        random.shuffle(Partie.choicesGive)
        for choix in Partie.choicesGive:
            lignes.append("{} - {}".format(count,'\n  + '.join(choix.choices)))
            count += 1  
        nrep = max(1,int(Partie.joueurs.nombre/3))
        await Joueur.name.send("Tiens, {} , voici un rappel de la phrase à compléter (Attention vous n'avez que {} secondes): \n- `{}`\n\nEt voici les cartes qu'on proposé les autres joueurs : \n```{}``` Réponds en envoyant ici les numéros des **{}** réponses que tu préfères séparés par des espaces".format(Joueur.name.name,timer,Partie.question.carte,'\n'.join(lignes),nrep))
        numbers = await AttendsRep(Joueur,count,nrep,Partie,True)
        for i in range(len(numbers)):
            numbers[i] = Partie.choicesGive[numbers[i]-1]
        Partie.choicesTake = numbers

######################### 

    async def ChoixGiveAll(Partie):

        async def Collect(Partie,joueur):
            if joueur != Partie.lead:
                await ChoixGive(Partie,joueur)
                Partie.choicesGive.append(joueur.pick)
                joueur.pick = None

        for joueur in Partie.joueurs.list:
            bot.loop.create_task(Collect(Partie,joueur))
            await asyncio.sleep(1)
            

#########################

    async def AfficheScore(ctx,Partie):
        resultats = []
        for i in range(len(Partie.joueurs.list)):
            Joueur = Partie.joueurs.list[i]
            resultats.append("{} - {} avec {} points".format(i+1,Joueur.name.name,Joueur.score))
        await ctx.send("```Voici les scores\n{}```".format('\n'.join(resultats)))

#########################

    async def Fin(ctx,Partie):
        k = 100
        lignes = []
        for i in range(len(Partie.choicesTake)):
            gg = Partie.choicesTake[i]
            Joueur = gg.joueur
            Joueur.score += k
            if i == 0:
                Partie.lead = Joueur
            lignes.append("`{} - {} ({} points)`\n  -> {}".format(i+1,Joueur.name,Joueur.score,filltrou(Partie.question.carte,gg.choices)))
            k = int(k*2/3)
        Partie.choicesGive = []
        await ctx.send("-----------------\nLes vainqueurs sont : \n{}\n-----------------------------".format('\n'.join(lignes)))

        Partie.joueurs.list.sort(key=attrgetter("score"),reverse=True)
        await AfficheScore(ctx,Partie)

#########################

    def PrintWaitingList(Partie):
        Repondu = []
        Manquant_Name = []
        for choice in Partie.choicesGive:
            Repondu.append(choice.joueur)

        Manquant = [x for x in Partie.joueurs.list if x not in Repondu]

        for joueur in Manquant:
            Manquant_Name.append(joueur.name.name)
        return Manquant_Name

#########################

    async def Tour(ctx,Joueurs,tour):
        Partie.pileQ.defausse.append(Partie.pileQ.pile[0])
        Partie.question = Question(Partie.pileQ.pile.pop(0))

        await ctx.send("Tour numéro : {}/{} \n\n**{}** est le chef, c'est lui qui va décider si t'es drôle ou pas.\nLa phrase à compléter est : `{}`".format(tour,Partie.tourmax,Partie.lead.name.name,Partie.question.carte))
        await ChoixGiveAll(Partie)

        t = timer - 16
        await ctx.send("En attente de : {}. Il reste {} secondes".format(','.join(PrintWaitingList(Partie)),t))
        while len(Partie.choicesGive) != len(Partie.joueurs.list) - 1:
            message = await ctx.channel.fetch_message(ctx.channel.last_message_id)
            await message.edit(content = "En attente de : {}. Il reste {} secondes".format(', '.join(PrintWaitingList(Partie)),t)) 
            await asyncio.sleep(1)
            t -= 1

        await asyncio.sleep(1)
        await message.edit(content = "En attente de : {}. Il a {} secondes".format(','.join(PrintWaitingList(Partie)),timer)) 
        bot.loop.create_task(ChoixTake(Partie))

        t = timer 
        while Partie.choicesTake == None :
            await message.edit(content = "En attente de : {}. Il reste {} secondes".format(','.join(PrintWaitingList(Partie)),t)) 
            await asyncio.sleep(1)
            t -= 1
        await message.delete()
        await Fin(ctx,Partie)

#########################

    member_list = ctx.channel.members
    member_list = [x for x in member_list if not x.bot]

    timer = 80

    Partie = init_partie(member_list,nbtour,categorie)

    for joueur in Partie.joueurs.list:
        joueur.main.append("**JOKER**")
    await ctx.send("La partie débute, elle durera **{}** tours.\n-----------------------".format(Partie.tourmax))
    for i in range(1,Partie.tourmax+1):
        await Tour(ctx,Partie,i)

    Exaequo = [x for x in Partie.joueurs.list if x.score == Partie.joueurs.list[0].score]
    if len(Exaequo) > 1:
        Partie.lead = random.choice([x for x in Partie.joueurs.list if x not in Exaequo])
        Partie.joueurs.list = Exaequo
        Partie.joueurs.list.append(Partie.lead)
        plist = [x.name.name for x in Exaequo]
        await ctx.send("------------------------------\nLes joueurs : {} sont a exaequo, une derniere manche à lieu juste entre eux pour les départager (les autres n'ont pas besoin de jouer)".format(','.join(plist),Partie.tourmax))
        await Tour(ctx,Partie,"SURSIS")

    # if Partie.joueurs.list[0].score == Partie.joueurs.list[1].score:
    #     await Tour(ctx,Partie,"SURSIS")
    await ctx.send("La partie est terminé, bien joué !")

################################################## 


@bot.command(name='bravery',aliases=['ub','ultimatebravery','challenge'], help='-> Ultimate Bravery',hidden=True) # Ultimate Bravery
@commands.check(isowner)
async def bravery(ctx, difficulte: int = 2, carte : str = "aram", *args):
    if len(args) == 0:
        args = ''
    img = DisplayUB(difficulte,carte,args)
    img.save('./imgub/ub.png', 'PNG')
    await ctx.send(file=discord.File('./imgub/ub.png'))

@bot.command(name='dice',aliases=['chance','luck'], help='-> Dame chance nous sourit\n(max des = 10, max cotes = 20)',hidden=True) # Lance nd dès à nc faces 
@commands.check(isowner)
async def roll(ctx, nombre_de_des: int, nombre_de_côtes: int):
    nd = min(nombre_de_des,10)
    nc = min(nombre_de_côtes,20)
    dès = [
        str(random.choice(range(1, nc + 1)))
        for _ in range(nd)
    ]
    await ctx.send(', '.join(des))

# ------------------------ Images -----------------------

@bot.command(name='img',hidden=True)
@commands.check(isowner)
async def img(ctx):
	await ctx.send(file=discord.File('./images/tuteur.png'))

# ------------------------ Voice ------------------------

@bot.command(pass_context=True,hidden=True)
@commands.check(isowner)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(pass_context=True,hidden=True)
@commands.check(isowner)
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_paused():
        await voice.pause()

@bot.command(pass_context=True,hidden=True)
@commands.check(isowner)
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()

@bot.command(pass_context=True,hidden=True)
@commands.check(isowner)
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.stop()

@bot.command(pass_context=True,hidden=True)
@commands.check(isowner)
async def leave(ctx):
    voice_bot = ctx.message.guild.voice_client
    await voice_bot.disconnect()

@bot.command(name="musiclist",aliases = ["ml","mlist"],pass_context=True,hidden=True)
@commands.check(isowner)
async def musiclist(ctx):
    dir = os.listdir("./musiques")
    await ctx.send('Musiques déjà présentes :\n{}'.format(', '.join(dir)))

@bot.command(name="musicbomb", aliases=["mb","bomb"],hidden=True)
@commands.check(isowner)
async def musicbomb(ctx,member: discord.Member, source: str):
    source = "./musiques/" + source + ".mp3"
    if os.path.isfile(source):
        channel = ctx.message.author.voice.channel
        voice_bot = ctx.message.guild.voice_client
        await channel.connect()
        voice = get(bot.voice_clients, guild=ctx.guild)
        await voice.play(discord.FFmpegPCMAudio(source),after = lambda x : asyncio.run_coroutine_threadsafe(ctx.message.guild.voice_client.disconnect(),ctx.message.guild.voice_client.loop))
    else:
        await ctx.send("Cette musique n'est pas présente dans le dossier")

@bot.command(name="dlmusic", aliases=["dlm"], hidden=True)
@commands.check(isowner)
async def dlmusic(ctx,url: str, nom: str):
    nom += ".mp3"
    ydl_opts = {
        'outtmpl': 'musiques/' + nom,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    if os.path.isfile(nom):
        os.remove(nom)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ------------------------ Exceptions ------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("T'as pas les droits :/")

# -------------- Lancer le Bot

bot.run(TOKEN)