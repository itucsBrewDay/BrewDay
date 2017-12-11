import unittest

from database import database
from Recipe import Recipe
from user import UserLogin


class RecipeTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test_incrementClick(self):
        recipe = Recipe.get_recipe(1)
        a = recipe.clickCount
        recipe.increment_clickcount()
        b = recipe.clickCount
        self.assertEqual(a,b-1)

    def test_getrecipe(self):
        recipeone = Recipe.get_recipe(1)
        self.assertEqual(recipeone.id, 1)


    def test_get_all(self):
        database.create_tables()
        UserLogin.add_user('test', 'test', 'test', 'test', 'test')
        user = UserLogin.select_user('test')
        Recipe.add(user, 'test', 1, 'test', 0, 0, 0)
        Recipe.add(user, 'test2', 1, 'test2', 0, 0, 0)
        Recipe.add(user, 'test3', 1, 'test2', 0, 0, 0)
        recipes = Recipe.getall()
        self.assertTrue(name in [x.name for x in recipes] for name in ['test','test2','test3'])








if __name__ == '__main__':
    unittest.main()