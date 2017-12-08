import psycopg2 as dbapi2
import json
import re
import os


class Database:
    def __init__(self):

        VCAP_SERVICES = os.getenv('VCAP_SERVICES')

        if VCAP_SERVICES is not None:
            self.config = Database.get_elephantsql_dsn(VCAP_SERVICES)
        else:
            self.config = """user='postgres' password='12345'
                            host='localhost' port=5432 dbname='BrewDay'"""

    @classmethod
    def get_elephantsql_dsn(cls, vcap_services):
        """Returns the data source name for ElephantSQL."""
        parsed = json.loads(vcap_services)
        uri = parsed["elephantsql"][0]["credentials"]["uri"]
        match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
        user, password, host, _, port, dbname = match.groups()
        dsn = """user='{}' password='{}' host='{}' port={}
                 dbname='{}'""".format(user, password, host, port, dbname)
        return dsn

    def create_tables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS UserInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE UserInfo (
                                                              UserID SERIAL PRIMARY KEY,
                                                              Mail varchar(100)  NOT NULL,
                                                              Name varchar(100)  NOT NULL,
                                                              Surname varchar(100)  NOT NULL,
                                                              UserName varchar(100)  NOT NULL,
                                                              Password varchar(500)  NOT NULL,
                                                              Date timestamp NOT NULL,
                                                              LastLoginDate timestamp,
                                                              CreateDate timestamp  NOT NULL
                                                            )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS TypeParameter CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE TypeParameter (
                                                              ID SERIAL PRIMARY KEY,
                                                              Name varchar(100)  NOT NULL
                                                            )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS EquipmentInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE EquipmentInfo (
                                                             ID SERIAL PRIMARY KEY,
                                                             UserID int  NOT NULL,
                                                             TypeID int  NOT NULL,
                                                             Size decimal(7,2)  NOT NULL,
                                                             CreateDate timestamp  NOT NULL,
                                                             FOREIGN KEY (TypeID) REFERENCES TypeParameter(ID),
                                                             FOREIGN KEY (UserID) REFERENCES UserInfo(UserID)
                            )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS RecipeInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE RecipeInfo (
                                                    RecipeID SERIAL PRIMARY KEY,
                                                    UserID int  NOT NULL,
                                                    CreateDate timestamp  NOT NULL,
                                                    Name varchar(100)  NOT NULL,
                                                    Description varchar(2000)  NOT NULL,
                                                    Procedure varchar(2000)  NOT NULL,
                                                    Clickcount int  DEFAULT 0,
                                                    FOREIGN KEY (UserID) REFERENCES UserInfo(UserID)
                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS IngredientParameter CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE IngredientParameter (
                                                  ID SERIAL PRIMARY KEY,
                                                  Name varchar(100)  NOT NULL
                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS RecipeMap CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE RecipeMap (
                                                  ID SERIAL PRIMARY KEY,
                                                  RecipeID int  NOT NULL,
                                                  IngredientID int  NOT NULL,
                                                  Amount decimal(7,2)  NOT NULL,
                                                  FOREIGN KEY (RecipeID) REFERENCES RecipeInfo(RecipeID) ON DELETE CASCADE,
                                                  FOREIGN KEY (IngredientID) REFERENCES IngredientParameter(ID)

                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS IngredientMap CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE IngredientMap (
                                                              ID SERIAL PRIMARY KEY,
                                                              UserID int  NOT NULL,
                                                              IngredientID int  NOT NULL,
                                                              Amount decimal(7,2)  NOT NULL,
                                                              FOREIGN KEY (UserID) REFERENCES UserInfo(UserID),
                                                              FOREIGN KEY (IngredientID) REFERENCES IngredientParameter(ID)

                                                            )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS RateCommentInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE RateCommentInfo (
                                                  ID SERIAL PRIMARY KEY,
                                                  RecipeID int  NOT NULL,
                                                  Rate int  NOT NULL,
                                                  Comment varchar(500)  NOT NULL,
                                                  UserID int  NOT NULL,
                                                  FOREIGN KEY (RecipeID) REFERENCES RecipeInfo(RecipeID)
                                                  FOREIGN KEY (UserID) REFERENCES UserInfo(UserID)

                                                )"""
            cursor.execute(query)

            connection.commit()
            cursor.close()

    def init_db(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            ### initialize the Parameter Types in ParameterType table. ###
            query = """INSERT INTO TypeParameter(Name) VALUES ('Boiler')"""
            cursor.execute(query)
            query = """INSERT INTO TypeParameter(Name) VALUES ('Mixer')"""
            cursor.execute(query)
            query = """INSERT INTO IngredientParameter(Name) VALUES ('Malt')"""
            cursor.execute(query)
            query = """INSERT INTO IngredientParameter(Name) VALUES ('Water')"""
            cursor.execute(query)
            query = """INSERT INTO IngredientParameter(Name) VALUES ('Sugar')"""
            cursor.execute(query)
            ##############################################################
database = Database()
