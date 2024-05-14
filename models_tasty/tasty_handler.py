import os
import json
from users.user_data import User


class TastyHandler:
    def __init__(
        self,
        tasty_file_path,
        videos_file_path,
        subs_file_path,
    ):
        self.display_callback = None
        self.details_callback = None
        self.all_recipes = []
        self.users_dir = "users"
        base_dir = "res"
        base_dir = os.path.dirname(os.path.realpath(__file__))
        self.tasty_file_path = os.path.join(base_dir, "..", "res", "tasty.json")
        self.videos_file_path = os.path.join(base_dir, "..", "res", "url.json")
        self.subs_file_path = os.path.join(base_dir, "..", "res", "subs.json")

        self.recipe_db = self.load_json(self.tasty_file_path)
        self.video_db = self.load_video_json(self.videos_file_path)
        self.substitutions_db = self.load_substitutions(self.subs_file_path)
        self.user = User()

    def load_json(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_video_json(self, filename):
        data = self.load_json(filename)
        return {
            self.normalize_name(item["name"]): item["video_url"]
            for item in data
            if "name" in item and "video_url" in item
        }

    def load_substitutions(self, filename):
        data = self.load_json(filename)
        return {item["Item"].lower(): item["Substitutions"] for item in data}

    def save_recipe_to_file_tasty(self, recipe_name, file_name="saved_recipes.json"):
        username = self.user.get_current_user()
        if not username:
            return "No user is currently logged in."

        recipe = self.recipe_db.get(recipe_name)
        if not recipe:
            return f"Recipe '{recipe_name}' not found."

        video_url = self.resolve_video_url(recipe_name)
        recipe_details = self.construct_recipe_details(recipe, recipe_name, video_url)
        return self.save_recipe_details(
            username, recipe_details, file_name, recipe_name
        )

    def resolve_video_url(self, recipe_name):
        video_url = self.video_db.get(recipe_name)
        if not video_url:
            return next(
                (
                    value
                    for key, value in self.video_db.items()
                    if key.lower() in recipe_name.lower()
                    or recipe_name.lower() in key.lower()
                ),
                "Video URL not available",
            )

    def construct_recipe_details(self, recipe, recipe_name, video_url):
        ingredients = [
            ingredient["name"]
            for section in recipe.get("ingredient_sections", [])
            for ingredient in section.get("ingredients", [])
        ]
        instructions = [
            instruction["display_text"]
            for instruction in recipe.get("instructions", [])
        ]
        return {
            "name": recipe_name,
            "url": video_url,
            "ingredients": ingredients,
            "instructions": instructions,
            "source": "Tasty",
        }

    def save_recipe_details(self, username, recipe_details, file_name, recipe_name):
        file_path = os.path.join(self.users_dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "r+", encoding="utf-8") as file:
                all_user_recipes = self.load_json_data(file_name)
                if username not in all_user_recipes:
                    all_user_recipes[username] = []
                all_user_recipes[username].append(recipe_details)
                self.update_recipe_file(file_name, all_user_recipes)
        except FileNotFoundError:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({username: [recipe_details]}, file, indent=4, ensure_ascii=False)
        return f"Recipe '{recipe_name}' has been saved successfully under user '{username}'."

    def update_recipe_file(self, file_name, all_user_recipes):
        file_path = os.path.join(self.users_dir, file_name)
        try:
            with open(file_path, "r+", encoding="utf-8") as file:
                file.seek(0)
                file.truncate()
                json.dump(all_user_recipes, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(all_user_recipes, file, indent=4, ensure_ascii=False)

    def load_json_data(self, file_name):
        """
        Attempts to load and return JSON data from a specified file.
        Returns an empty dictionary if the file cannot be read or found.
        """
        file_path = os.path.join(self.users_dir, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def normalize_name(self, name):
        return name.strip().lower()

    def load_tasty_recipes(self):
        """
        This method is used in the all_ui.py file specifically, for loading recipe details in a different GUI format.
        """
        try:
            with open(self.tasty_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    # Unpack each dictionary into the list with the recipe name and recipe details as other key value pairs
                    return [{"name": name, **details} for name, details in data.items()]
                else:
                    raise ValueError(
                        "Tasty recipes data is not in the expected dictionary format."
                    )
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading or processing {self.tasty_file_path}: {e}")
            return []


    def delete_recipe_by_name_tasty(self, recipe_name, file_name="saved_recipes.json"):
        username = self.user.get_current_user()
        if not username:
            return "No user is currently logged in."

        all_user_recipes = self.load_json_data(file_name)
        if not all_user_recipes or username not in all_user_recipes:
            return "Error reading saved recipes file or user not found."

        user_recipes = all_user_recipes.get(username, [])
        if recipe_name not in [recipe["name"] for recipe in user_recipes]:
            return f"Tasty recipe '{recipe_name}' not found under user '{username}'."

        updated_recipes = [recipe for recipe in user_recipes if recipe["name"] != recipe_name]
        all_user_recipes[username] = updated_recipes

        save_status = self.save_updated_recipes(file_name, all_user_recipes)
        return save_status if save_status != "Recipes updated successfully." else f"Tasty recipe '{recipe_name}' has been deleted successfully for username {username}."

    def save_updated_recipes(self, file_name, all_user_recipes):
        file_path = os.path.join(self.users_dir, file_name)
        try:
            with open(file_path, "r+", encoding="utf-8") as file:
                file.seek(0)
                file.truncate()
                json.dump(all_user_recipes, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            return "Error saving recipes file."

        return f"Recipes updated successfully."

    def set_display_callback(self, callback):
        self.display_callback = callback

    def set_details_callback(self, callback):
        self.details_callback = callback

    def on_recipe_selected(self, index):
        if index < len(self.all_recipes):
            source, selected_recipe = self.all_recipes[index]
            if self.details_callback:
                self.details_callback(selected_recipe, source)

