import psycopg2 as dbapi2
from database import database
import datetime
from user import *
from flask_login import  current_user

class Profile():
    def __init__(cls, id, username, name, surname, email):
        cls.id = id
        cls.username = username
        cls.name = name
        cls.surname = surname
        cls.email = email

    @classmethod
    def get_userInfo(cls,username):
        userInfo = None
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT Name,Surname,Mail,CreateDate,LastLoginDate,Username,UserID FROM UserInfo WHERE Username ='%s'""" %username

            try:
                cursor.execute(query)

            except dbapi2.Error:
                print("rollback ERROR")
                connection.rollback()
            else:
                print("ERROR")
                userInfo = cursor.fetchall()
                connection.commit()

            cursor.close()
        return userInfo

    @classmethod
    def update_userInfo(cls, userID,newUserInfo):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            try:
                if newUserInfo[0] != '':
                    query = """UPDATE UserInfo SET Name = '%s' WHERE userID = %d""" % (newUserInfo[0],int(userID))
                    cursor.execute(query)
                if newUserInfo[1] != '':
                    query = """UPDATE UserInfo SET Surname = '%s' WHERE userID = %d""" % (newUserInfo[1],int(userID))
                    cursor.execute(query)
                if newUserInfo[2] != '':
                    query = """UPDATE UserInfo SET Mail = '%s' WHERE userID = %d""" % (newUserInfo[2],int(userID))
                    cursor.execute(query)
                if newUserInfo[3] != '':
                    query = """UPDATE UserInfo SET Username = '%s' WHERE userID = %d""" % (newUserInfo[3],int(userID))
                    cursor.execute(query)
                if newUserInfo[4] != '':
                    hashp = pwd_context.encrypt(newUserInfo[4])
                    query = """UPDATE UserInfo SET Password = '%s' WHERE userID = %d""" % (hashp,int(userID))
                    cursor.execute(query)

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
                cursor.close()
            return True

    @classmethod
    def whatShouldIBrewToday(self):

        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userId = current_user.id
            query = """SELECT TOP 1 FROM RecipeInfo k, RecipeMap l, UserInfo m, IngredientMap x, RateCommentInfo y
                        WHERE k.RecipeID = l.RecipeID and y.RecipeID = k.RecipeID and m.ID = %s and x.UserID = %s and (l.IngredientID = x.IngredientID and x.Amount > l.Amount)
                        ORDER BY AVG(Rate) DESC"""%userId%userId

            try:
                cursor.execute(query, (userId,userId))

            except dbapi2.Error:
                connection.rollback()
            else:
                recipeInfo = cursor.fetchall()
                connection.commit()

            cursor.close()
        return recipeInfo
