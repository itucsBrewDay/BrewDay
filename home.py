from flask import Blueprint
from database import database
from user import *
import datetime
from passlib.apps import custom_app_context as pwd_context
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_user, current_user, login_required, logout_user

from user import UserLogin
from Recipe import Recipe
site = Blueprint('site',__name__)

@site.route('/initdb')
def initialize_database():

    database.create_tables()
    UserLogin.add_user("admin", "12345")
    Recipe.add(UserLogin.select_user("admin"), "Recipe1", "Descripion for Recipe1", "Procedure of Recipe1")
    Recipe.add(UserLogin.select_user("admin"), "Recipe2", "Descripion for Recipe2", "Procedure of Recipe2")
    Recipe.add(UserLogin.select_user("admin"), "Recipe3", "Descripion for Recipe3", "Procedure of Recipe3")
    Recipe.add(UserLogin.select_user("admin"), "Recipe4", "Descripion for Recipe4", "Procedure of Recipe4")
    Recipe.add(UserLogin.select_user("admin"), "Recipe5", "Descripion for Recipe5", "Procedure of Recipe5")
    Recipe.add(UserLogin.select_user("admin"), "Recipe6", "Descripion for Recipe6", "Procedure of Recipe6")

    return redirect(url_for('site.home_page'))

@site.route('/')
def home_page():
    recipes = Recipe.getall()
    print("Current user: ",current_user.is_authenticated)
    return render_template('home.html', recipes=recipes)

@site.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home_page'))

@site.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = UserLogin.select_user(request.form['username'])
        if user and user != -1:
            if pwd_context.verify(request.form['password'], user.password):
                UserLogin.setLastLoginDate(user)
                login_user(user)
                print("Current user:",current_user.username)
                return redirect(url_for('site.home_page'))


@site.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        UserLogin.add_user(request.form['username'], request.form['password'])
        return redirect(url_for('site.home_page'))

@site.route('/search_recipe', methods=['GET', 'POST'])
@login_required
def search_recipe():
    if request.method == 'GET':
        return render_template('search_recipe.html')
    else:
        pass # pass for now, will be implemented later
