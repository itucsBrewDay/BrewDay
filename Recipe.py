import psycopg2 as dbapi2
from database import database
import datetime
from user import *


class Recipe:
	def __init__(cls, id, user, cd, name, desc, procedure, clickCount):
		cls.id = id
		cls.user = user
		cls.createdate = cd
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
		count = 0
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
					recipes.append(Recipe(r[0], UserLogin.select_user_with_id(r[1]), r[2], r[3], r[4], r[5], r[6]))
			except dbapi2.Error as err:
				print("Recipe get_recent function Error:", err)
				connection.rollback()
			else:
				connection.commit()

			query = "SELECT COUNT(RecipeID) FROM RecipeInfo"

			try:
				cursor.execute(query)
				count = cursor.fetchone()[0]
			except dbapi2.Error as err:
				print("Recipe get_recent function Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return recipes, count

	@staticmethod
	def getall():
		recipes = []
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """SELECT r.*, AVG(rc.rate) FROM RecipeInfo as r LEFT JOIN RateCommentInfo as rc
						ON r.recipeid = rc.recipeid
						GROUP BY r.recipeid"""

			try:
				cursor.execute(query)
				for r in cursor:
					recipes.append(Recipe(r[0], UserLogin.select_user_with_id(r[1]), r[2], r[3], r[4], r[5], r[6]))
			except dbapi2.Error as err:
				print("Recipe getall Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return recipes

	@staticmethod
	def get_recipe(id):
		recipe = None
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """SELECT * FROM RecipeInfo where recipeid = %d""" %id

			try:
				cursor.execute(query)
				r = cursor.fetchone()
				recipe = Recipe(r[0],UserLogin.select_user_with_id(r[1]), r[2], r[3], r[4], r[5], r[6])

			except dbapi2.Error as err:
				print("Recipe get_recipe function Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return recipe

	@staticmethod
	def insert_rate_comment(recipeid, rate, comment, userid):
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()

			query = "DELETE FROM RateCommentInfo WHERE RecipeID = %s AND userid = %s" % (recipeid, userid)
			try:
				cursor.execute(query)
			except dbapi2.Error as err:
				print("delete rate comment Error:", err)
				connection.rollback()
			else:
				connection.commit()

			query = "INSERT INTO RateCommentInfo (recipeid, rate, comment, userid) VALUES (%d,%s,'%s',%d)" % (recipeid, rate, comment, userid)
			try:
				cursor.execute(query)
			except dbapi2.Error as err:
				print("insert_rate_comment Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()

	def get_score(self): # implemented as method rather than a class variable because the score can be changed externally
		score = 0
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = "SELECT AVG(Rate) FROM RateCommentInfo WHERE RecipeID = %d" % self.id
			try:
				cursor.execute(query)
				score = cursor.fetchone()[0]
			except dbapi2.Error as err:
				print("get_score Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		if score is None:
			score = 0
		return float("{0:.2f}".format(score))

	def get_ingredients(self):
		ingredients = {}
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """SELECT i.name, m.amount FROM ingredientparameter as i, recipemap as m 
					   WHERE m.ingredientid = i.id AND m.recipeid = %d""" % self.id
			try:
				cursor.execute(query)
				for i in cursor:
					ingredients[i[0]] = i[1]
			except dbapi2.Error as err:
				print("Recipe get_ingredients Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()
		return ingredients

	def increment_clickcount(self):
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """UPDATE RecipeInfo set clickcount = clickcount + 1 where recipeid = %d""" % self.id
			try:
				cursor.execute(query)
				self.clickCount += 1
			except dbapi2.Error:
				connection.rollback()
			else:
				connection.commit()

			cursor.close()

	def get_user_rate(self, userid):
		rate = 0
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = "SELECT Rate FROM RateCommentInfo WHERE RecipeID = %d AND userid = %s" % (self.id, userid)
			try:
				cursor.execute(query)
				rate = cursor.fetchone()
				if rate is not None:
					rate = rate[0]
				else:
					rate = 0
			except dbapi2.Error as err:
				print("get_user_rate Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()

		return rate

	def get_comments(self):
		comments = []
		with dbapi2.connect(database.config) as connection:
			cursor = connection.cursor()
			query = """SELECT u.username, r.rate, r.comment FROM UserInfo as u, RateCommentInfo as r
			        WHERE u.userid = r.userid AND r.recipeid = %d""" % self.id
			try:
				cursor.execute(query)
				for c in cursor:
					comments.append((c[0], c[1], c[2]))
			except dbapi2.Error as err:
				print("get_comments Error:", err)
				connection.rollback()
			else:
				connection.commit()

			cursor.close()

		return comments