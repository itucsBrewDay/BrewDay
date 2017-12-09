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
from Profile import Profile
from ingredient import IngredientDatabase, IngredientMapDatabase
from recipeV2 import RecipeDatabase, RecipeMapDatabase
from equipment import EquipmentDatabase, EquipmentTypeDatabase

site = Blueprint('site', __name__)


@site.route('/initdb')
def initialize_database():
    loremipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam et rutrum sem, nec scelerisque ex. Ut mollis, quam vitae eleifend ornare, sapien est semper magna, sed fermentum diam neque ac est. Praesent at cursus lorem. Ut metus leo, laoreet non bibendum in, efficitur nec nisi. Cras lobortis ut quam nec volutpat. Fusce massa lectus, varius eget magna eget, egestas lacinia sapien. Morbi eget tellus orci. Nullam egestas velit urna, eget porta dui vehicula nec. Integer aliquet, neque et viverra sagittis, turpis lorem facilisis nisl, vitae consectetur magna erat at orci. Praesent fermentum justo erat. Duis tincidunt, eros nec ullamcorper molestie, odio magna viverra urna, quis tincidunt tortor nisl id nisl. Sed ut erat sit amet quam ultrices posuere.'
    database.create_tables()
    database.init_db()
    UserLogin.init_admin()
    for r in range(1, 19):
        Recipe.add(UserLogin.select_user("admin"), "Recipe%r" % r, loremipsum, "Procedure of Recipe%r" % r)

    return redirect(url_for('site.home_page'))


@site.route('/<int:pagenumber>')
def home_page_number(pagenumber):
    if pagenumber < 1:
        pagenumber = 1
    if pagenumber > 3:
        pagenumber = 3
    recipes = Recipe.get_recents(6, 6 * (pagenumber - 1))
    for recipe in recipes:
        recipe.desc = recipe.desc[:200]  # anasayfada sadece max 150 kararkter göster
        if recipe.desc[-1] == ' ':
            recipe.desc = recipe.desc[:-1]
        recipe.desc += "..."

    return render_template('home.html', recipes=recipes, current_page=pagenumber)


@site.route('/')
def home_page():
    return redirect('/1')

@site.route('/recipe/<int:recipeID>')
@login_required
def show_recipe(recipeID):
        recipe = Recipe.get_recipe(recipeID)
        recipe.increment_clickcount()
        ingredients = Recipe.get_ingredients(recipe);
        return render_template('recipe.html', recipe=recipe,ingredients=ingredients)


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
                return redirect(url_for('site.home_page'))


@site.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    else:

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if password == confirm:
            UserLogin.add_user(name, surname, email, username, password)
        else:
            pass  # will be implemented later

        return redirect(url_for('site.login_page'))

@site.route('/search_recipe', methods=['GET', 'POST'])
@login_required
def search_recipe():
    if request.method == 'GET':
        return render_template('search_recipe.html', recipes=Recipe.getall())

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    if request.method == 'GET':
        userInfo = Profile.get_userInfo(current_user.username)

        status = UserLogin.get_status(userInfo[0][6])
        recipes = Profile.getUserRecipe()
        ingredients = IngredientMapDatabase.getAllIngredientsOfUser()
        equipments = EquipmentDatabase.getEquipmentOfUser()
        recipeDic = Profile.whatShouldIBrewToday()
        recipe_suggestions = []

        if recipeDic:
            recipe_suggestions.append(list(recipeDic.keys())[0])
            recipe_suggestions.append(list(recipeDic.values())[0])
        return render_template('profile.html', userInfo=userInfo, recipes=recipes, ingredients=ingredients, recipe_suggestions = recipe_suggestions,
                               equipments=equipments, status=status)


@site.route('/profile/delete/<int:recipeID>/', methods=['GET', 'POST'])
@login_required
def profile_recipe_delete(recipeID):

    if request.method == 'POST':
        Profile.deleteRecipe(recipeID)

    return redirect(url_for('site.profile_page'))


@site.route('/profile/apply/<int:recipeID>', methods=['GET', 'POST'])
@login_required
def profile_apply_recipe(recipeID):

    retval = Profile.recipeApply(recipeID)
    return redirect(url_for('site.profile_page'))


@site.route('/profile/edit/<int:userID>/', methods=['GET', 'POST'])
@login_required
def profile_edit(userID):

    if request.method == 'GET':
        userInfo = Profile.get_userInfo(current_user.username)

        return render_template('profile_edit.html', userInfo=userInfo)
    else:
        newUserInfo = []

        newUserInfo.append(request.form['name'])
        newUserInfo.append(request.form['surname'])
        newUserInfo.append(request.form['email'])
        newUserInfo.append(request.form['username'])
        newUserInfo.append(request.form['password'])

        Profile.update_userInfo(userID, newUserInfo=newUserInfo)
        return redirect(url_for('site.profile_page'))


@site.route('/profile/add', methods=['GET', 'POST'])
@login_required
def profile_recipe_add():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()

    if request.method == 'GET':
        ingredients = IngredientDatabase.getAllIngredients()

        return render_template('profile_recipe_add.html', ingredients=ingredients)
    # query = """ SELECT ID,NAME FROM PARAMETERTYPE WHERE ID='%d'"""% TYPE
    # cursor.execute(query)
    # typeName = cursor.fetchone()


    # return render_template('parameter_add.html', user=current_user.username, parameterType=typeName)
    else:
        recipeName = request.form['recipeName']
        description = request.form['description']
        procedure = request.form['procedure']

        ingredient_list = IngredientDatabase.getAllIngredients()
        ingredientIdList = []
        for k in ingredient_list:
            ingredientIdList.append(k[0])

        ingredient = []
        for i in ingredientIdList:
            ingredientid = "ingredient{}".format(str(i))

            ingredient.append(request.form[ingredientid])

        recipeID = RecipeDatabase.addRecipe(recipeName, description, procedure)
        for i in ingredientIdList:
            RecipeMapDatabase.addRecipe(recipeID, i, ingredient[i - 1])
        # query = "INSERT INTO PARAMETERS(TYPEID,NAME) VALUES('%d', '%s')" % (TYPE, parameterName)
        # cursor.execute(query)

        # connection.commit()

        return redirect(url_for('site.profile_page'))


        # parameterName = request.form['parameterType']
        #
        #
        # query = "INSERT INTO PARAMETERS(TYPEID,NAME) VALUES('%d', '%s')" % (TYPE,parameterName)
        # cursor.execute(query)
        #
        # connection.commit()
        #
        # return redirect(url_for('site.parameters_page'))


@site.route('/profile/ingredientAdd', methods=['GET', 'POST'])
@login_required
def profile_ingredient_add():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()

    if request.method == 'GET':
        ingredients = IngredientDatabase.getAllIngredients()

        return render_template('profile_ingredient_add.html', ingredients=ingredients)
    else:
        ingredient_list = IngredientDatabase.getAllIngredients()
        ingredientIdList = []
        for k in ingredient_list:
            ingredientIdList.append(k[0])

        ingredient = []
        for i in ingredientIdList:
            ingredientid = "ingredient{}".format(str(i))

            ingredient.append(request.form[ingredientid])

        for i in ingredientIdList:
            IngredientMapDatabase.ingredientAddOrUpdate(i, ingredient[i - 1])

        return redirect(url_for('site.profile_page'))


@site.route('/profile/equipmentAdd', methods=['GET', 'POST'])
@login_required
def profile_equipment_add():
    with dbapi2.connect(database.config) as connection:
        cursor = connection.cursor()
    if request.method == 'GET':
        equipments = EquipmentTypeDatabase.getEquipmentTypes()
        return render_template('profile_equipment_add.html', equipments=equipments)
    else:
        equipment_list = EquipmentTypeDatabase.getEquipmentTypes()
        equipmentIdList = []
        for k in equipment_list:
            equipmentIdList.append(k[0])

        equipment = []
        for i in equipmentIdList:
            equipmentid = "equipment{}".format(str(i))
            equipment.append(request.form[equipmentid])
        for i in equipmentIdList:
            EquipmentDatabase.equipmentAddOrUpdate(i, equipment[i - 1])

        return redirect(url_for('site.profile_page'))

