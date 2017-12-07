import psycopg2 as dbapi2
from database import database
from flask_login import current_user


class Ingredient:
    def __init__(self, id, name):
        self.ID = id
        self.name = name


class IngredientDatabase:
    @classmethod
    def addIngredientParameter(cls, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO IngredientParameter (name) VALUES (%s)"""
            cursor.execute(query, (name,))
            cursor.close()

    @classmethod
    def getAllIngredients(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM IngredientParameter """

            try:
                cursor.execute(query)
                ingredientInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if ingredientInfo:
                return Ingredient(ID=ingredientInfo[0], name=ingredientInfo[1],)
            else:
                return -1

    @classmethod
    def deleteIngredientParameter(cls, id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM IngredientParameter where ID = %s"""

        try:
            cursor.execute(query, (id,))
        except dbapi2.Error as err:
            print("Ingredient Delete Error:", err)
            connection.rollback()
        else:
            connection.commit()

        cursor.close()