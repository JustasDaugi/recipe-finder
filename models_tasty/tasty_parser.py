import json
import re
import os
from models_tasty.tasty_handler import TastyHandler


class TastyParser:
    def __init__(self):
        self.handler = TastyHandler("tasty.json", "url.json", "subs.json")
        self.users_dir = "users"

    def parse_ingredients(self, food_input, spice_input):
        if ',' not in (food_input + spice_input) and '.' not in (food_input + spice_input):
            food_input += ","
        if ',' in (food_input + spice_input) or '.' in (food_input + spice_input):
            if '.' in (food_input + spice_input):
                return False
            else:
                return [
                    i.strip().lower() for i in (food_input + "," + spice_input).split(",") if i
                ]
        return []

    def find_matching_recipes(self, user_ingredients):
        matches = self.get_matches(user_ingredients)
        return [self.prepare_match_for_display(m) for m in matches] if matches else []

    def get_matches(self, user_ingredients):
        # Calls evaluate_match for each recipe
        matches = [
            self.evaluate_match(rn, rd, user_ingredients)
            for rn, rd in self.handler.recipe_db.items()
            if self.evaluate_match(rn, rd, user_ingredients)
            is not None
        ]
        # Returns a sorted list of tuples
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def evaluate_match(self, recipe_name, recipe_data, user_ingredients):
        score, matches_count, matched_ingredients = self.calculate_score(
            recipe_data, user_ingredients
        )
        total_ingredients = len(self.extract_ingredient_names(recipe_data))

        if matches_count > 0:
            substitutions = self.find_substitutions(
                matched_ingredients, recipe_data, user_ingredients
            )
            return (
                recipe_name,
                matches_count / total_ingredients,
                matched_ingredients,
                substitutions,
                total_ingredients,
            )

    def extract_ingredient_names(self, recipe_data):
        return [
            ingredient_data["name"].lower()
            for section in recipe_data.get("ingredient_sections", [])
            for ingredient_data in section.get("ingredients", [])
            if ingredient_data.get("name")
        ]

    def calculate_score(self, recipe_data, user_ingredients):
        score = 0
        matched_ingredients = set()
        for user_ingredient in user_ingredients:
            ingredient_pattern = self.get_ingredient_pattern(user_ingredient)
            for ingredient_name in self.extract_ingredient_names(recipe_data):
                if ingredient_pattern.search(ingredient_name):
                    matched_ingredients.add(user_ingredient)
                    score += 1
                    break
        return score, len(matched_ingredients), list(matched_ingredients)

    def get_ingredient_pattern(self, user_ingredient):
        # Checks if a match starts at a word boundary or after a non-digit character
        return re.compile(
            rf"(?:\b|\D){re.escape(user_ingredient.rstrip('s').rstrip('es'))}(?:e|es|s)?\b",
            re.IGNORECASE,
        )

    def find_substitutions(self, matched_ingredients, recipe_data, user_ingredients):
        # Filters out recipe_data by using get_relevant_ingredients
        relevant_ingredients = self.get_relevant_ingredients(
            recipe_data, matched_ingredients, user_ingredients
        )
        return {
            ing: self.find_ingredient_substitution(ing) for ing in relevant_ingredients
        }
        
    def find_ingredient_substitution(self, ingredient):
        for sub, sub_list in self.handler.substitutions_db.items():
            if sub in ingredient or ingredient in sub:
                return sub_list
            
    def get_relevant_ingredients(
        self, recipe_data, matched_ingredients, user_ingredients
    ):
        """
        Identifies ingredients from the recipe that need substitutions. 
        Excludes matched and closely related user ingredients.
        
        Returns:
            set: A set of ingredient names from the recipe that require substitutions.
        """
        recipe_ingredient_names = self.extract_ingredient_names(recipe_data)
        user_ingredients_lower = {ing.lower() for ing in user_ingredients}
        matched_ingredients_lower = {ing.lower() for ing in matched_ingredients}
        return {
            ing
            for ing in recipe_ingredient_names
            if not self.is_close_match(ing, user_ingredients_lower)
            and ing not in matched_ingredients_lower
        }

    def prepare_match_for_display(self, match):
        recipe_name, _, matched_ingredients, substitutions, _ = match
        normalized_recipe_name = self.handler.normalize_name(recipe_name)
        recipe_data = self.handler.recipe_db[recipe_name]
        video_url = self.handler.video_db.get(
            normalized_recipe_name, "URL not available"
        )
        # Returns a list of tuples for each variable
        return (recipe_name, recipe_data, matched_ingredients, substitutions, video_url)

    def is_close_match(self, ingredient, user_ingredients):
        # Checks for user ingredient in recipe ingredients or recipe ingredients in users input(ing in ingredient) 
        return any(ing in ingredient or ingredient in ing for ing in user_ingredients)


    def search_recipe_by_name_tasty(self, recipe_name):
        normalized_recipe_name = self.handler.normalize_name(recipe_name)

        for current_recipe_name, recipe_data in self.handler.recipe_db.items():
            normalized_current_name = self.handler.normalize_name(current_recipe_name)
            if normalized_current_name == normalized_recipe_name:
                return {
                    "name": current_recipe_name,
                    "data": self.get_recipe_content(recipe_data),
                }
        return {"message": f"Recipe '{recipe_name}' not found in the database."}

    def get_recipe_content(self, recipe):
        ingredients = [
            ingredient["name"]
            for section in recipe.get("ingredient_sections", [])
            for ingredient in section.get("ingredients", [])
        ]

        instructions = [
            instruction["display_text"]
            for instruction in recipe.get("instructions", [])
        ]

        return ingredients, instructions

    def get_saved_recipes_for_display(self, username, file_name="saved_recipes.json"):
        """
        Retrieves and formats saved recipes for a specific user from a JSON file.
        """
        file_path = os.path.join(self.users_dir, file_name)
        all_user_recipes = self.load_user_recipes(file_path)
        if not all_user_recipes:
            return "No saved recipes found in the specified file."

        user_recipes = all_user_recipes.get(username, [])
        if not user_recipes:
            return "No saved recipes found."

        tasty_recipes = self.filter_and_format_tasty_recipes(user_recipes)
        return "\n\n".join(tasty_recipes) if tasty_recipes else "No Tasty recipes found for this user."

    def load_user_recipes(self, file_path):
        """
        Attempts to load and return the recipes from the given file path.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def filter_and_format_tasty_recipes(self, user_recipes):
        """
        Filters recipes that are from 'Tasty' and formats them for display.
        """
        tasty_formatted_recipes = []
        for recipe in user_recipes:
            if recipe.get("source", "Unknown") == "Tasty":
                tasty_formatted_recipes.append(self.format_recipe_for_display(recipe))
        return tasty_formatted_recipes

    def format_recipe_for_display(self, recipe):
        """
        Formats a single recipe into a string for display.
        """
        recipe_details = f"Recipe: {recipe['name']}\nURL: {recipe.get('url', 'URL not available')}\nIngredients:\n"
        recipe_details += "\n".join(f" - {ingredient}" for ingredient in recipe.get("ingredients", []))
        recipe_details += "\nInstructions:\n"
        instructions = recipe.get("instructions", ["No instructions available."])
        recipe_details += "\n".join(f" - {instruction}" for instruction in instructions)
        return recipe_details

    def run(self):
        user_ingredients = self.parse_ingredients(
            input("Enter ingredients: "), input("Enter spices: ")
        )
        recipes = self.find_matching_recipes(user_ingredients)
        print(recipes)


if __name__ == "__main__":
    finder = TastyParser()
    finder.run()

