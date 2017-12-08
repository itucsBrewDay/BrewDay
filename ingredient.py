import psycopg2 as dbapi2
from database import database
from flask_login import current_user


class IngredientParameter:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Ingredient:
    def __init__(self, id, userId, ingredientId, amount):
        self.id = id
        self.userId = userId
        self.ingredientId = ingredientId
        self.amount = amount


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
                ingredientInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


            return ingredientInfo


    @classmethod
    def getIngredientName(cls,id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM IngredientParameter WHERE ID = %s""" %id

            try:
                cursor.execute(query,(id))
                ingredientInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if ingredientInfo:
                return IngredientParameter(ID=ingredientInfo[0], name=ingredientInfo[1], )
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


class IngredientMapDatabase:
    @classmethod
    def addIngredient(cls, userID, ingredientID, amount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO IngredientMap (userID,ingredientID,amount) VALUES (%s,%s,%s)"""
            cursor.execute(query, (userID,ingredientID,amount))
            cursor.close()

    @classmethod
    def getAllIngredientsOfUser(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userID = current_user.id
            query = """SELECT * FROM IngredientMap WHERE UserID = %s"""%userID

            try:
                cursor.execute(query,(userID))
                ingredientInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if ingredientInfo:
                return IngredientParameter(ID=ingredientInfo[0], userId=ingredientInfo[1], ingredientId=ingredientInfo[2], amount=ingredientInfo[3],)
            else:
                return -1

    @classmethod
    def updateIngredientOfUser(cls, newAmount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userID = current_user.id
            try:
                for i in newAmount:
                    query = """UPDATE IngredientMap SET Amount = '%s' WHERE UserID = %s and IngredientID = %s""" %(i[1],userID,i[0])
                    cursor.execute(query)


            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
                cursor.close()
            return True