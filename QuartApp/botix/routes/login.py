from quart import Blueprint, render_template, redirect, url_for
from quart_auth import *

import json

loginBP = Blueprint('login', __name__)

passwordPath = './QuartApp/botix/static/password.txt'

@loginBP.route("/")
async def login(password=""):
    if not current_user.auth_id :
        return await render_template('login.html')
    else : 
        logout_user()
        return redirect("/botix/place_publique")

@loginBP.route("/insert/<password>")
async def login_mdp(password=""):
    
    if password != "" :
        try : 
            with open(passwordPath) as json_file:
                mdp_dic = json.load(json_file)
        except : 
            mdp_dic = []

        for key, mdp_list in mdp_dic.items():
            if password in mdp_list :
                login_user(user=AuthUser(int(key)),remember=True)

    if not current_user.auth_id :
        return redirect("/botix/login")
    else : 
        return redirect("/botix/place_publique")

@loginBP.route("/logout")
async def logout():
    logout_user()
    return redirect("/botix/place_publique")
    
@loginBP.route("/restrict")
@login_required
async def restricted_route():
    print(current_user.auth_id) # Will be 2 given the login_user code above
    return "Non connecté"