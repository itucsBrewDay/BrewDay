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
    def addEquipment(cls, typeID, size):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userId = current_user.id
            CreateDate = datetime.datetime.now()
            query = """INSERT INTO EquipmentInfo (userID, typeID, size, CreateDate) VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (userId, typeID, size, CreateDate,))
            cursor.close()

    @classmethod
    def getEquipmentOfUser(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            userID = current_user.id
            query = """SELECT * FROM EquipmentInfo WHERE UserID=%s """

            try:
                cursor.execute(query, (userID,))
                equipmentInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if equipmentInfo:
                return Equipment(ID=equipmentInfo[0], userID=equipmentInfo[1], typeID=equipmentInfo[2], size=equipmentInfo[3],
                              createDate=equipmentInfo[4],)
            else:
                return -1

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