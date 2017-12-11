import unittest
from user import UserLogin
from Recipe import Recipe
from database import database


class RecipeTest(unittest.TestCase):

    def test_getstatus_norecipe(self):
        database.create_tables()
        UserLogin.add_user('test','test','test','test','test')
        user = UserLogin.select_user('test')
        status = UserLogin.get_status(int(user.get_id()))
        self.assertEqual("Beginner Brewer",status)

    def test_getstatus_noscore(self):
        database.create_tables()
        UserLogin.add_user('test','test','test','test','test')
        user = UserLogin.select_user('test')
        Recipe.add(user, 'test', 1, 'test', 0, 0, 0)
        Recipe.add(user, 'test', 1, 'test', 0, 0, 0)
        status = UserLogin.get_status(int(user.get_id()))
        self.assertEqual("Beginner Brewer",status)

    def test_getstatus_score_3(self):
        database.create_tables()
        UserLogin.add_user('test','test','test','test','test')
        user = UserLogin.select_user('test')
        Recipe.add(user, 'test', 1, 'test', 0, 0, 0)
        Recipe.insert_rate_comment(1,3,'test',int(user.get_id()))
        status = UserLogin.get_status(int(user.get_id()))
        self.assertEqual("Intermediate Brewer",status)

    def test_getstatus_score_5(self):
        database.create_tables()
        UserLogin.add_user('test','test','test','test','test')
        user = UserLogin.select_user('test')
        Recipe.add(user, 'test', 1, 'test', 0, 0, 0)
        Recipe.insert_rate_comment(1,5,'test',int(user.get_id()))
        status = UserLogin.get_status(int(user.get_id()))
        self.assertEqual("Master Brewer",status)





