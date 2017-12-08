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

	@staticmethod
	def add(user, name, desc, procedure, malt=0, water=0, sugar=0): # eklenen Recipe'leri uygun map'lere de ekle!!!
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """INSERT INTO RecipeInfo ( userid, Name, description, procedure, clickcount, CreateDate) VALUES (%s,%s,%s,%s,%s,%s) RETURNING recipeid"""
			recipeid = None
			try:
				cursor.execute(query, (user.id, name, desc, procedure, 0, datetime.datetime.now()))
				recipeid = cursor.fetchone()[0]
			except dbapi2.Error as err:
				print("Recipe Add Error:", err)
				connection.rollback()
			else:
				connection.commit()

			query = """INSERT INTO RecipeMap (recipeid, ingredientid, amount) VALUES (%s,%s,%s)"""

			if recipeid is not None:
				for (i, amount) in [(1, malt), (2, water), (3, sugar)]:
					try:
						cursor.execute(query, (recipeid, i, amount))
					except dbapi2.Error as err:
						print("Recipe Ingredient Map Add Error:", err)
						connection.rollback()
					else:
						connection.commit()

			cursor.close()

	@staticmethod
	def get_recents(limit = None, offset = None):
		recipes = []
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """	SELECT * FROM 
							(SELECT r.*, AVG(m.Rate) as score FROM RecipeInfo as r LEFT JOIN RateCommentInfo as m
								ON r.recipeid = m.recipeid 
								GROUP BY r.recipeid
								ORDER BY createdate desc"""
			if limit is not None:
				query += " limit %r" % limit
			if offset is not None:
				query += " offset %r" % offset
			query += """	) as sub
						ORDER BY sub.score desc NULLS LAST"""
			try:
				cursor.execute(query)
				for r in cursor:
					recipes.append(Recipe(r[0], UserLogin.select_user_with_id(r[1]), r[3], r[4], r[5], r[6]))
			except dbapi2.Error as err:
				print("Recipe getall function Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return recipes

	@staticmethod
	def get_like(like):
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

	def get_score(self):
		score = 0
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = "SELECT AVG(Rate) FROM RateCommentInfo WHERE RecipeID = %d" % self.id
			try:
				cursor.execute(query)
				score = cursor.fetchone()[0]
			except dbapi2.Error:
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		if score is None:
			score = 0
		return score

	def get_ingredients(self):
		ingredients = {}
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """SELECT i.name, m.amount FROM ingredientparameter as i, recipemap as m 
					   WHERE m.ingredientid = i.id AND m.recipeid = %d AND m.amount > 0""" % self.id
			try:
				cursor.execute(query)
				for i in cursor:
					ingredients[i[0]] = i[1]
			except dbapi2.Error:
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return ingredients