import unittest

from Recipe import Recipe


class RecipeTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test_incrementClick(self):
        recipe = Recipe.get_recipe(1)
        a = recipe.clickCount
        recipe.increment_clickcount()
        b = recipe.clickCount
        self.assertEqual(a,b-1)




if __name__ == '__main__':
    unittest.main()