import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user


class ProfileRecipe():
    def __init__(self, userID, createDate, name, description, procedure, clickcount):
        self.userID = userID
        self.createDate = createDate
        self.name = name
        self.description = description
        self.procedure = procedure
        self.clickcount = clickcount


class RecipeMap():
    def __init__(self, ID, recipeID, ingredientID, amount):
        self.ID = ID
        self.recipeID = recipeID
        self.ingredientID = ingredientID
        self.amount = amount


class RecipeDatabase:
    @classmethod
    def addRecipe(cls, name, description,procedure):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userId = current_user.id
            createDate = datetime.datetime.now()
            query = """INSERT INTO RecipeInfo (userId, createDate, name, description,procedure ,clickcount) VALUES (%s, %s, %s, %s, %s , %s)"""
            cursor.execute(query, (userId, createDate, name, description,procedure ,0,))
            query = """SELECT * FROM RecipeInfo ORDER BY CREATEDATE DESC"""
            cursor.execute(query)
            lastrow = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
            return lastrow




class RecipeMapDatabase:
    @classmethod
    def addRecipe(cls, recipeID, ingredientID, amount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RecipeMap (recipeID,ingredientID,amount) VALUES (%s,%s,%s)"""
            cursor.execute(query, (recipeID,ingredientID,amount))
            connection.commit()
            cursor.close()

