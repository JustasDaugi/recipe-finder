import os
import json
from users.user_data import User


class BBCFileHandler:
    def __init__(self, bbc_file_path, subs_file_path):
        self.users_dir = "users"
        base_dir = os.path.dirname(os.path.realpath(__file__))
        self.bbc_file_path = os.path.join(base_dir, '..', 'res', "bbc.json")
        self.subs_file_path = os.path.join(base_dir, '..', 'res', "subs.json")
        self.recipe_db = self.load_recipes_from_file(self.bbc_file_path)
        self.substitutions_db = self._load_substitutions(self.subs_file_path)
        self.user = User()

    def load_recipes_from_file(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {file_name}: {e}")
            return []
        
    def _load_substitutions(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return {item["Item"].lower(): item["Substitutions"] for item in data}

    def load_bbc_recipes(self):
        return self.load_recipes_from_file(self.bbc_file_path)

    def _get_recipe_details(self, recipe):
        return {
            "name": recipe.get("name"),
            "url": recipe.get("url", "URL not available"),
            "ingredients": recipe.get("ingredients", []),
            "steps": recipe.get("steps", []),
            "source": "BBC Goodfood",
        }

    def load_user_recipes(self, file_path, username=None):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if username:
            if username not in data:
                data[username] = []
        return data

    def save_recipe_to_file(self, recipe, file_name="saved_recipes.json"):
        username = self.user.get_current_user()
        if not username:
            return "No user is currently logged in."

        recipe_details = self._get_recipe_details(recipe)
        file_path = os.path.join(self.users_dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        all_user_recipes = self.load_user_recipes(file_path, username)
        # Append the recipe to the username list in the dictionary of recipes
        all_user_recipes[username].append(recipe_details)
        self._write_user_recipes(all_user_recipes, file_path)
        return f"Recipe '{recipe_details['name']}' has been saved successfully under user '{username}'."

    def _write_user_recipes(self, all_user_recipes, file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(all_user_recipes, file, indent=4, ensure_ascii=False)

    def view_saved_recipes(self, file_name="saved_recipes.json"):
        username = self.user.get_current_user()
        file_path = os.path.join(self.users_dir, file_name)
        saved_recipes = self.load_user_recipes(file_path)
        return self._format_saved_recipes(saved_recipes.get(username, []))

    def _format_saved_recipes(self, user_recipes):
        if not user_recipes:
            return "No recipes found."

        bbc_recipes = []
        tasty_recipes = []
        for recipe in user_recipes:
            formatted_recipe = self._format_recipe(recipe)
            if recipe.get("source") == "BBC Goodfood":
                bbc_recipes.append(formatted_recipe)
            elif recipe.get("source") == "Tasty":
                tasty_recipes.append(formatted_recipe)

        bbc_output = "\n" + "\n\n".join(bbc_recipes) if bbc_recipes else ""
        return bbc_output + "\n\n"

    def _format_recipe(self, recipe):
        ingredients = "\n".join(
            f" - {ingredient}" for ingredient in recipe.get("ingredients", [])
        )
        steps = "\n".join(recipe.get("steps", []))
        return f"Name: {recipe['name']}\nURL: {recipe.get('url', 'URL not available')}\nIngredients:\n{ingredients}\nSteps:\n{steps}\n"


    def delete_recipe_by_name(self, recipe_name, file_name="saved_recipes.json"):
        username = self.user.get_current_user()
        file_path = os.path.join(self.users_dir, file_name)
        all_user_recipes = self.load_user_recipes(file_path, username)
        recipe_index = self._find_recipe_index(all_user_recipes[username], recipe_name)
        if recipe_index is None:
            return f"Recipe '{recipe_name}' not found."
        del all_user_recipes[username][recipe_index]
        # Overwrite the file without the recipe that was selected to delete
        self._write_user_recipes(all_user_recipes, file_path)
        return f"Recipe '{recipe_name}' has been deleted successfully under username {username}."

    def _find_recipe_index(self, user_recipes, recipe_name):
        return next(
            (
                i
                for i, recipe in enumerate(user_recipes)
                if recipe["name"] == recipe_name
            ),
            None,
        )
