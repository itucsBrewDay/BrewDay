import psycopg2 as dbapi2
from database import database
import datetime

class Recipe:
    def __init__(self, id, user, name, desc, procedure):
        self.id = id
        self.user = user
        self.name = name
        self.desc = desc
        self.procedure = procedure

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
