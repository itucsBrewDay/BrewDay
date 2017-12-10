from flask_login import UserMixin
import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime

class User(UserMixin):
    def __init__(self, id, username, password, lastLoginDate):
        self.id = id
        self.username = username
        self.password = password
        self.lastLoginDate = lastLoginDate

class UserLogin:

    @classmethod
    def init_admin(self):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            LastLoginDate = datetime.datetime.now()
            password = '12345'
            hashp = pwd_context.encrypt(password)
            ### initialize the admin user in UserInfo table. ###
            query = """INSERT INTO UserInfo(Mail,name,surname,username,password,date,LastLoginDate,CreateDate) VALUES ('admin@brewday.com','admin','admin','admin','%s','5.12.2017', '%s', '5.12.2017')""" % (hashp,LastLoginDate)
            cursor.execute(query)

        ##############################################################
            connection.commit()
            cursor.close()

    @classmethod
    def add_user(cls, name, surname, email, username, password):
        with dbapi2.connect(database.config) as connection:

            cursor = connection.cursor()
            hashp = pwd_context.encrypt(password)
            query = "INSERT INTO UserInfo( Mail, Name, Surname, UserName, Password, Date, LastLoginDate, CreateDate) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (email, name, surname, username, hashp,datetime.datetime.now(),datetime.datetime.now(), datetime.datetime.now())

            try:
                cursor.execute(query)

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM UserInfo WHERE username='%s' """ % username

            user_data = None

            try:
                cursor.execute(query)
                user_data = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0],  username=user_data[4], password=user_data[5],  lastLoginDate = user_data[7])
            else:
                return None

    @classmethod
    def select_user_with_id(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM UserInfo WHERE UserID='%s'""" % user_id

            try:
                cursor.execute(query)
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[4], password=user_data[5], lastLoginDate = user_data[7])
            else:
                return -1

    @classmethod
    def setLastLoginDate(cls, user):
        user.lastLoginDate = datetime.datetime.now()
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE UserInfo SET LastLoginDate =%s WHERE (UserID = %s)"""
            cursor.execute(query, (datetime.datetime.now(), user.id,))
            connection.commit()
            cursor.close()

    @classmethod
    def get_status(cls, userid):
        status = 0
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT AVG(k.rate) FROM RateCommentInfo as k, RecipeInfo as l WHERE k.RecipeID = l.RecipeID and l.UserID = %s """%(userid)

            try:
                cursor.execute(query)
            except dbapi2.Error as err:
                connection.rollback()
            else:
                status = cursor.fetchone()
                connection.commit()
            statusValue = status[0]
            cursor.close()
            print(statusValue)
        if statusValue is None:
            statusValue = 0
        if 1 <= float(statusValue) < 2.5:
            return "Beginner Brewer"
        elif 2.5 <= float(statusValue) < 4:
            return "Intermediate Brewer"
        elif 4 <= float(statusValue) <= 5:
            return "Master Brewer"
        else:
            return ""