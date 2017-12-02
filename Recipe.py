import psycopg2 as dbapi2
from database import database
import datetime
from user import *

class Recipe:
    def __init__(self, id, user, name, desc, procedure, clickCount):
        self.id = id
        self.user = user
        self.name = name
        self.desc = desc
        self.procedure = procedure
        self.clickCount = clickCount

    def add(self, user, name, desc, procedure):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RecipeInfo ( userid, Name, description, procedure, clickcount, CreateDate) VALUES (%s,%s,%s,%s,%s,%s)"""

            try:
                cursor.execute(query, (user.id, name, desc, procedure, 0, datetime.datetime.now()))

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    def getall(self):
        recipes = []
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RecipeInfo"""

            try:
                cursor.execute(query)
                for r in cursor:
                    recipes.append(Recipe(r[0], User.select_user_with_id(r[1]), r[3], r[4], r[5], r[6]))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
        return recipes