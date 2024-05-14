import unittest
from unittest.mock import patch
from models_tasty.tasty_parser import TastyParser
import re


class TestRecipeFinder(unittest.TestCase):
    def setUp(self):
        self.tasty_parser = TastyParser()

    def test_parse_ingredients(self):
        result = self.tasty_parser.parse_ingredients("flour, tomato", "cheese")
        self.assertListEqual(result, ["flour", "tomato", "cheese"])
        result = self.tasty_parser.parse_ingredients("flour. tomato", "cheese")
        self.assertFalse(result)

        result = self.tasty_parser.parse_ingredients("flour", "cheese")
        self.assertListEqual(result, ["flour", "cheese"])

        result = self.tasty_parser.parse_ingredients("", "")
        self.assertListEqual(result, [])

    @patch.object(TastyParser, "extract_ingredient_names")
    @patch.object(TastyParser, "is_close_match")
    def test_get_relevant_ingredients(
        self, mock_is_close_match, mock_extract_ingredient_names
    ):
        mock_extract_ingredient_names.return_value = ["flour", "sugar", "eggs", "milk"]

        mock_is_close_match.side_effect = lambda ing, user_ingredients: ing in [
            "flour",
            "sugar",
        ]

        recipe_data = {}
        matched_ingredients = ["flour"]
        user_ingredients = ["flour", "sugar", "milk"]

        result = self.tasty_parser.get_relevant_ingredients(
            recipe_data, matched_ingredients, user_ingredients
        )

        expected_result = {"eggs", "milk"}
        self.assertSetEqual(result, expected_result)

    @patch.object(TastyParser, "extract_ingredient_names")
    def test_calculate_score(self, mock_extract_ingredient_names):
        mock_extract_ingredient_names.return_value = ["flour", "sugar", "eggs"]

        recipe_data = {}
        user_ingredients = ["flour", "sugar"]

        score, matches_count, matched_ingredients = self.tasty_parser.calculate_score(
            recipe_data, user_ingredients
        )

        self.assertEqual(score, 2)
        self.assertEqual(matches_count, 2)
        self.assertListEqual(matched_ingredients, ["flour", "sugar"])

    def test_extract_ingredient_names(self):
        recipe_data = {
            "ingredient_sections": [
                {
                    "ingredients": [
                        {"name": "flour"},
                        {"name": "sugar"},
                        {"name": "eggs"},
                    ]
                }
            ]
        }

        result = self.tasty_parser.extract_ingredient_names(recipe_data)
        self.assertListEqual(result, ["flour", "sugar", "eggs"])

    def test_get_ingredient_pattern(self):
        user_ingredient = "flour"
        pattern = self.tasty_parser.get_ingredient_pattern(user_ingredient)
        self.assertIsInstance(pattern, re.Pattern)
        self.assertTrue(pattern.search("flour"))
        self.assertFalse(pattern.search("sugar"))


if __name__ == "__main__":
    unittest.main()
