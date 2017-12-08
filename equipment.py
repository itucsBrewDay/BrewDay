import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user


class Equipment():
    def __init__(self, ID, userID, typeID, size, createDate):
        self.ID = ID
        self.userID = userID
        self.typeID = typeID
        self.size = size
        self.createDate = createDate

class EquipmentDatabase:
    @classmethod
    def equipmentAddOrUpdate(cls, typeID, size):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userID = current_user.id
            query = """SELECT COUNT(*) FROM EquipmentInfo WHERE UserID = %s and typeID = %s"""
            cursor.execute(query, (str(userID), str(typeID)))
            count = cursor.fetchone()
            if count[0] == 0:
                query = """INSERT INTO EquipmentInfo (userID,typeID,size,createDate) VALUES (%s,%s,%s,%s)"""
                cursor.execute(query, (userID,typeID,size,datetime.datetime.now()))
            else:
                query = """UPDATE EquipmentInfo SET size = '%s' WHERE UserID = %s and typeID = %s""" % (size, userID, typeID)
                cursor.execute(query)
            connection.commit()
            cursor.close()

    @classmethod
    def getEquipmentOfUser(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userID = current_user.id
            query = """SELECT l.name, k.size FROM EquipmentInfo as k, TypeParameter as l WHERE k.TypeID = l.ID and UserID=%s """%(userID)
            try:
                cursor.execute(query)
                equipmentInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return equipmentInfo

    @classmethod
    def deleteEquipmentOfUser(cls, id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM EquipmentInfo where ID = %s"""

        try:
            cursor.execute(query, (id,))
        except dbapi2.Error as err:
            print("Equipment Delete Error:", err)
            connection.rollback()
        else:
            connection.commit()

        cursor.close()

class EquipmentTypeDatabase:
    @classmethod
    def getEquipmentTypes(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userID = current_user.id
            query = """SELECT * FROM TypeParameter """
            try:
                cursor.execute(query)
                equipmentInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return equipmentInfo