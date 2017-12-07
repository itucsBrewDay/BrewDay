import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user


class Recipe():
    def __init__(self, userID, createDate, name, description, procedure, clickcount):
        self.userID = userID
        self.createDate = createDate
        self.name = name
        self.description = description
        self.procedure = procedure
        self.clickcount = clickcount

class RecipeDatabase:
    @classmethod
    def addRecipe(cls, name, description,procedure):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userId = current_user.id
            createDate = datetime.datetime.now()
            query = """INSERT INTO EquipmentInfo (userId, createDate, name, description,procedure ,clickcount) VALUES (%s, %s, %s, %s, %s , %s)"""
            cursor.execute(query, (userId, createDate, name, description,procedure ,0,))
            return cursor.lastrowid
            cursor.close()

