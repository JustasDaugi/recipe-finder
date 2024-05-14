import re
from models_bbc.bbc_handler import BBCFileHandler


class BBCParser:
    def __init__(self):
        self.handler = BBCFileHandler("bbc.json", "subs.json")

    def parse_ingredients(self, food_input, spice_input):
        if "," not in (food_input + spice_input) or "." in (food_input + spice_input):
            return False

        ingredients = (food_input + "," + spice_input).split(",")
        return [ingredient.strip().lower() for ingredient in ingredients if ingredient]

    def find_matching_recipes(self, user_ingredients):
        """Finds and ranks recipes based on the number of matched ingredients."""
        matches = self._gather_matches(user_ingredients)
        return self._sort_matches(matches)

    def _gather_matches(self, user_ingredients):
        """Gather all matches based on user ingredients."""
        matches = []
        for recipe in self.handler.recipe_db:
            score, matches_count, matched_ingredients, total_ingredients = self._calculate_score(recipe, user_ingredients)
            updated_recipe = self._update_recipe_with_matches(recipe, matched_ingredients, total_ingredients)
            self._add_substitutions(updated_recipe, recipe, matched_ingredients, user_ingredients)
            matches.append(updated_recipe)
        return matches

    def _update_recipe_with_matches(self, recipe, matched_ingredients, total_ingredients):
        """Updates the recipe dictionary with match details."""
        updated_recipe = recipe.copy()
        updated_recipe["matched_ingredients"] = matched_ingredients
        updated_recipe["total_ingredients"] = total_ingredients
        return updated_recipe

    def _add_substitutions(self, updated_recipe, recipe, matched_ingredients, user_ingredients):
        """Adds substitutions to the recipe if any are found."""
        substitutions = self._get_substitutions(recipe.get("ingredients", []), matched_ingredients, user_ingredients)
        if substitutions:
            updated_recipe["substitutions"] = substitutions

    def _sort_matches(self, matches):
        """Sorts matches based on the proportion and number of matched ingredients."""
        return sorted(
            matches,
            key=lambda x: (len(x["matched_ingredients"]) / x["total_ingredients"], len(x["matched_ingredients"])),
            reverse=True
        )

    def _calculate_score(self, recipe, user_ingredients):
        """Calculate matching score based on user ingredients and recipe ingredients."""
        score, matched_ingredients = self._match_ingredients(recipe, user_ingredients)
        total_ingredients = len(recipe.get("ingredients", []))
        return (
            score,
            len(matched_ingredients),
            list(matched_ingredients),
            total_ingredients
        )
        
    def _match_ingredients(self, recipe, user_ingredients):
        """Match user ingredients to recipe ingredients and calculate score."""
        matched_ingredients = set()
        score = 0
        user_ingredients_lower = [ingredient.lower() for ingredient in user_ingredients]

        for user_ingredient in user_ingredients_lower:
            ingredient_pattern = self._create_ingredient_pattern(user_ingredient)
            for recipe_ingredient in recipe.get("ingredients", []):
                recipe_ingredient_lower = recipe_ingredient.lower()
                if ingredient_pattern.search(recipe_ingredient_lower):
                    score += 1
                    matched_ingredients.add(user_ingredients[user_ingredients_lower.index(user_ingredient)])
                    break
        return score, matched_ingredients

    def _create_ingredient_pattern(self, ingredient):
        """Create a regular expression pattern to match an ingredient considering its plural forms."""
        return re.compile(rf"\b{re.escape(ingredient)}(es|s)?\b", re.IGNORECASE)

    def _get_substitutions(
        self, recipe_ingredients, matched_ingredients, user_ingredients
    ):
        """
        Determines possible substitutions for ingredients not matched with user's ingredients.

        Parameters:
            recipe_ingredients (list): Ingredients in the recipe.
            matched_ingredients (list): User's ingredients that match the recipe ingredients.
            user_ingredients (list): All ingredients entered by the user.

        Returns:
            dict: Maps ingredients with no matches in users input to their possible substitutions.
        """
        user_ingredients_lower = set(
            ingredient.lower() for ingredient in user_ingredients
        )
        matched_ingredients_lower = set(
            ingredient.lower() for ingredient in matched_ingredients
        )

        def is_close_match(ingredient, user_ingredients):
            for user_ingredient in user_ingredients:
                if user_ingredient in ingredient or ingredient in user_ingredient:
                    return True
            return False

        relevant_ingredients = {
            ingredient
            for ingredient in recipe_ingredients
            if not is_close_match(ingredient, user_ingredients_lower)
            and ingredient not in matched_ingredients_lower
        }

        substitutions = {}
        for ingredient in relevant_ingredients:
            # For key, value in the json substitutions file:
            for sub, sub_list in self.handler.substitutions_db.items():
                if sub in ingredient or ingredient in sub:
                    substitutions[ingredient] = sub_list
                    break

        return substitutions

    def search_recipe_by_name(self, recipe_name):
        normalized_recipe_name = recipe_name.strip().lower()
        for recipe in self.handler.recipe_db:
            db_recipe_name = recipe.get("name", "").strip().lower()
            if normalized_recipe_name == db_recipe_name:
                return recipe
        return {"message": f"Recipe '{recipe_name}' not found in the database."}

    def run(self, food_input, spice_input):
        user_ingredients = self.parse_ingredients(food_input, spice_input)
        recipes = self.find_matching_recipes(user_ingredients)
        if recipes:
            first_recipe = recipes[0]
            save_message = self.handler.save_recipe_to_file(first_recipe)
            print(save_message)
        else:
            print("No matching recipes found.")


if __name__ == "__main__":
    parser = BBCParser()
    user_ingredients = parser.parse_ingredients()
    parser.run(user_ingredients)
