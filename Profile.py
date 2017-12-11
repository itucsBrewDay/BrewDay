import psycopg2 as dbapi2
from database import database
import datetime
from user import *
from itertools import groupby
from flask_login import current_user


class Profile():
    def __init__(cls, id, username, name, surname, email):
        cls.id = id
        cls.username = username
        cls.name = name
        cls.surname = surname
        cls.email = email

    class ProfileRecipeInfo():
        def __init__(cls, id, name, description, procedure, ingredient, amount):
            cls.id = id
            cls.name = name
            cls.description = description
            cls.procedure = procedure
            cls.ingredient = ingredient
            cls.amount = amount

    @classmethod
    def get_userInfo(cls, username):
        userInfo = None
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT Name,Surname,Mail,CreateDate,LastLoginDate,Username,UserID FROM UserInfo WHERE Username ='%s'""" % username

            try:
                cursor.execute(query)

            except dbapi2.Error as err:
                print("get_userInfo ERROR:", err)
                connection.rollback()
            else:
                userInfo = cursor.fetchall()
                connection.commit()

            cursor.close()
        return userInfo

    @classmethod
    def update_userInfo(cls, userID, newUserInfo):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            try:
                if newUserInfo[0] != '':
                    query = """UPDATE UserInfo SET Name = '%s' WHERE userID = %d""" % (newUserInfo[0], int(userID))
                    cursor.execute(query)
                if newUserInfo[1] != '':
                    query = """UPDATE UserInfo SET Surname = '%s' WHERE userID = %d""" % (newUserInfo[1], int(userID))
                    cursor.execute(query)
                if newUserInfo[2] != '':
                    query = """UPDATE UserInfo SET Mail = '%s' WHERE userID = %d""" % (newUserInfo[2], int(userID))
                    cursor.execute(query)
                if newUserInfo[3] != '':
                    query = """UPDATE UserInfo SET Username = '%s' WHERE userID = %d""" % (newUserInfo[3], int(userID))
                    cursor.execute(query)
                if newUserInfo[4] != '':
                    hashp = pwd_context.encrypt(newUserInfo[4])
                    query = """UPDATE UserInfo SET Password = '%s' WHERE userID = %d""" % (hashp, int(userID))
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
            query = """SELECT COUNT (*) FROM RateCommentInfo """
            try:
                cursor.execute(query)

            except dbapi2.Error:
                connection.rollback()

            else:
                count = cursor.fetchone()
                connection.commit()
            if count[0] == 0:
                query = """SELECT k.RecipeID, l.name, l.description, l.procedure, y.name, k.amount  FROM IngredientMap as x, IngredientParameter as y, RecipeMap as k, RecipeInfo as l
                                  WHERE x.UserID = %d and x.IngredientID = y.ID and k.IngredientID = x.IngredientID and k.RecipeID = l.RecipeID and x.amount >= k.amount
                                    
                                      """ % (userId)
                try:
                    cursor.execute(query)

                except dbapi2.Error:
                    connection.rollback()

                else:
                    recipeInfo = cursor.fetchall()
                    connection.commit()
            else:
                query = """SELECT k.RecipeID
                            FROM IngredientMap as x, IngredientParameter as y, RecipeMap as k, RecipeInfo as l, RateCommentInfo as a
                                    WHERE x.UserID = %d and x.IngredientID = y.ID and k.IngredientID = x.IngredientID and k.RecipeID = l.RecipeID and x.amount >= k.amount and l.RecipeID = a.RecipeID
                                      GROUP BY k.recipeID
                                              ORDER BY AVG(a.rate) DESC""" % (userId)
                try:
                    cursor.execute(query)

                except dbapi2.Error:
                    connection.rollback()

                else:
                    recipeIDs = cursor.fetchone()
                    connection.commit()
                    if recipeIDs is not None:
                        recipeID = recipeIDs[0]
                    else:
                        recipeID = None

                if recipeID is None:
                    return None

                query = """SELECT k.RecipeID, l.name, l.description, l.procedure, y.name, k.amount
                            FROM IngredientParameter as y, RecipeMap as k, RecipeInfo as l, RateCommentInfo as a
                                WHERE y.ID = k.IngredientID and k.RecipeID = l.RecipeID and l.RecipeID = a.RecipeID and a.RecipeID = '%s'
                                                      """ % (recipeID)
                try:
                    cursor.execute(query)

                except dbapi2.Error as err:
                    connection.rollback()

                else:
                    recipeInfo = cursor.fetchall()
                    connection.commit()


            query = """SELECT * FROM IngredientParameter """
            try:
                cursor.execute(query)

            except dbapi2.Error:
                connection.rollback()

            else:
                ingredient = cursor.fetchall()
                connection.commit()
            cursor.close()
            d = dict()
            merge = True
            newList = []
            ctrl = 1
            counter = 1
            for j in recipeInfo:
                for i in ingredient:
                    if i[1] == j[4]:
                        ctrl = ctrl + 1

                if ctrl == 4:
                    newList.append(j[0])
                if counter == 4:
                    ctrl = 1
                    counter = 1

            for recipe in recipeInfo:
                if recipe[0] in newList:
                    k = recipe[0]
                    v = d.get(k, tuple()) + (recipe[:0] + recipe[0 + 1:] if merge else (recipe[:0] + recipe[0 + 1:],))
                    d.update({k: v})

            return d


    @classmethod
    def getUserRecipe(self):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userId = current_user.id
            recipeInfo = None
            query = """SELECT k.RecipeID, k.name, k.description, k.procedure, m.name, l.amount
                            FROM RecipeInfo as k, RecipeMap as l, IngredientParameter as m 
                             WHERE k.RecipeID = l.RecipeID  AND l.IngredientID = m.ID and k.userID = %d
                             """ % (userId)
            try:
                cursor.execute(query)

            except dbapi2.Error:
                # print("ROLLBACK ERROR")
                connection.rollback()
            else:
                recipeInfo = cursor.fetchall()
                connection.commit()
            list = [[] for a in range(50)]
            j = 0
            k = 0
            lastID = 0
            for i in recipeInfo:

                if j == 0:
                    list[0].append(i)
                    lastID = i[0]
                    j = 1
                else:
                    if i[0] == lastID:
                        list[k].append(i)
                    else:
                        k = k + 1
                        list[k].append(i)
                        lastID = i[0]
            cursor.close()
        return list


    @classmethod
    def deleteRecipe(self, recipeID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM RECIPEMAP WHERE recipeID= '%d'" % (recipeID)
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
                # print("RollBack Error")
            else:
                connection.commit()
            query = "DELETE FROM RECIPEINFO WHERE recipeID= '%d'" % (recipeID)

            try:
                cursor.execute(query)
            except dbapi2.Error:

                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return


    @classmethod
    def recipeApply(self, recipeID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT IngredientID, Amount FROM RecipeMap WHERE RecipeID = %d""" % (recipeID)
            try:
                cursor.execute(query)

            except dbapi2.Error:
                connection.rollback()
            else:
                recipeIngredientInfo = cursor.fetchall()
                connection.commit()

            userId = current_user.id
            query = """SELECT IngredientID, Amount FROM IngredientMap WHERE UserID = %d""" % (userId)

            try:
                cursor.execute(query)

            except dbapi2.Error:
                connection.rollback()
            else:
                userIngredientInfo = cursor.fetchall()
                connection.commit()

        if len(recipeIngredientInfo) > len(userIngredientInfo):
            return "Not enough ingredients"

        ctrl = 0
        for i in recipeIngredientInfo:
            for j in userIngredientInfo:
                if i[0] == j[0]:
                    if i[1] > j[1]:
                        ctrl = 1

        if ctrl == 1:
            return "Not enough ingredients"
        else:
            for i in recipeIngredientInfo:
                for j in userIngredientInfo:
                    if i[0] == j[0]:
                        query = """UPDATE IngredientMap SET Amount = %s WHERE IngredientID = %s"""

                        try:
                            cursor.execute(query, (j[1] - i[1], i[0]))

                        except dbapi2.Error:
                            connection.rollback()
                        else:
                            connection.commit()
            cursor.close()
            return "Successfully Applied"
