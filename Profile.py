import psycopg2 as dbapi2
from database import database
import datetime
from user import *

class Profile:
    def __init__(self, id, username, name, surname, email):
        self.id = id
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email



    @classmethod
    def get_userInfo(self,username):

        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT Name,Surname,Mail,CreateDate,LastLoginDate FROM UserInfo WHERE username ='%s'""" %username

            try:
                cursor.execute(query)

            except dbapi2.Error:
                connection.rollback()
            else:
                userInfo = cursor.fetchall()
                connection.commit()

            cursor.close()
        return userInfo