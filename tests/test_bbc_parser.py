import unittest
from unittest.mock import MagicMock
from models_bbc.bbc_parser import BBCParser

class TestBBCParser(unittest.TestCase):
    def setUp(self):
        self.bbc_recipes = BBCParser()
        self.bbc_recipes.handler = MagicMock()
        self.bbc_recipes.handler.recipe_db = [
            {"name": "pizza", "ingredients": ["flour", "tomato", "cheese"]}
        ]

    def test_parse_ingredients(self):
        food_input = "flour, sugar"
        spice_input = "salt, pepper"
        result = self.bbc_recipes.parse_ingredients(food_input, spice_input)
        expected_result = ["flour", "sugar", "salt", "pepper"]
        self.assertListEqual(result, expected_result)

    def test_search_recipe_by_name(self):
        recipe_name = "pizza"
        result = self.bbc_recipes.search_recipe_by_name(recipe_name)
        expected_result = {
            "name": "pizza",
            "ingredients": ["flour", "tomato", "cheese"],
        }
        self.assertDictEqual(result, expected_result)

    def test_search_recipe_by_name_not_found(self):
        recipe_name = "tacos"
        result = self.bbc_recipes.search_recipe_by_name(recipe_name)
        expected_result = {"message": "Recipe 'tacos' not found in the database."}
        self.assertDictEqual(result, expected_result)

    def test_calculate_score(self):
        recipe = {"ingredients": ["flour", "sugar", "tomato", "cheese"]}

        user_ingredients = ["flour", "sugar", "tomato", "cheese"]
        score, matched_count, matched_ingredients, total_ingredients = (
            self.bbc_recipes._calculate_score(recipe, user_ingredients)
        )
        expected_score = 4
        expected_matched_count = 4
        expected_matched_ingredients = ["flour", "sugar", "tomato", "cheese"]
        expected_total_ingredients = 4

        self.assertEqual(score, expected_score)
        self.assertEqual(matched_count, expected_matched_count)
        self.assertTrue(set(matched_ingredients) == set(expected_matched_ingredients))
        self.assertEqual(total_ingredients, expected_total_ingredients)


if __name__ == "__main__":
    unittest.main()
