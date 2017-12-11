import unittest

from Recipe import Recipe
from user import UserLogin


class RecipeTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test_incrementClick(self):
        UserLogin.add_user('test','test','test','test','test')
        user = UserLogin.select_user('test')
        Recipe.add(user,'test',1,'test',0,0,0)
        recipe = Recipe.get_recipe(1)
        a = recipe.clickCount
        recipe.increment_clickcount()
        b = recipe.clickCount
        self.assertEquals(a,b-1)




if __name__ == '__main__':
    unittest.main()