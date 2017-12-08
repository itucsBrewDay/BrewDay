import psycopg2 as dbapi2
from database import database
import datetime
from user import *


class Recipe:
	def __init__(cls, id, user, name, desc, procedure, clickCount):
		cls.id = id
		cls.user = user
		cls.name = name
		cls.desc = desc
		cls.procedure = procedure
		cls.clickCount = clickCount

	@classmethod
	def add(cls, user, name, desc, procedure):
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """INSERT INTO RecipeInfo ( userid, Name, description, procedure, clickcount, CreateDate) VALUES (%s,%s,%s,%s,%s,%s)"""

			try:
				cursor.execute(query, (user.id, name, desc, procedure, 0, datetime.datetime.now()))
			except dbapi2.Error as err:
				print("Recipe Add Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()

	@classmethod
	def getall(cls, limit = None, offset = None):
		recipes = []
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """SELECT * FROM RecipeInfo"""
			if limit is not None:
				query += " limit %r" % limit
			if offset is not None:
				query += " offset %r" % offset
			try:
				cursor.execute(query)
				for r in cursor:
					recipes.append(Recipe(r[0], UserLogin.select_user_with_id(r[1]), r[3], r[4], r[5], r[6]))
			except dbapi2.Error:
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return recipes

	@classmethod
	def get_like(cls, like):
		recipes = []
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """SELECT * FROM RecipeInfo where name like '%s%%' OR description like '%%%s%%'""" % (like, like)

			try:
				cursor.execute(query)
				for r in cursor:
					recipes.append(Recipe(r[0], UserLogin.select_user_with_id(r[1]), r[3], r[4], r[5], r[6]))
			except dbapi2.Error as err:
				print("Recipe get_like Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return recipes
