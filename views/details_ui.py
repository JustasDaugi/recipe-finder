import tkinter as tk
from models_tasty.tasty_handler import TastyHandler

class DetailsUI:
    def __init__(self, root, display):
        self.root = root
        self.handler = TastyHandler("tasty.json", "url.json", "subs.json")
        self.display = display

    def process_selected_recipe(self, index):
        from search_ui import SearchUI
        self.display = SearchUI()
        if index < len(self.display.recipes):
            source, selected_recipe = self.display.recipes[index]
            if self.display.selected_database.lower() == "bbc_goodfood":
                self.populate_recipe_details_bbc(selected_recipe)
            elif self.display.selected_database.lower() == "tasty":
                self.display_recipe_details(selected_recipe)
            else:
                print("Unknown recipe source")

    def on_recipe_selected(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            if index < len(self.display.recipes):
                selected_recipe = self.display.recipes[index]
                if self.display.selected_database == "bbc_goodfood":
                    self.populate_recipe_details_bbc(selected_recipe)
                else:
                    self.display_recipe_details(selected_recipe)

    def display_recipe_details(self, recipe):
        recipe_name = recipe_data = matched_ingredients = substitutions = video_url = None

        if not isinstance(recipe, tuple):
            self.populate_recipe_details_bbc(recipe)
            return
        
        num_elements = len(recipe)
        if num_elements == 2:
            _, recipe_dict = recipe
            recipe_name = recipe_dict.get("name", "No Name")
            recipe_data = recipe_dict
            matched_ingredients = []
            substitutions = {}
        elif num_elements == 5:
            recipe_name, recipe_data, matched_ingredients, substitutions, video_url = recipe
        else:
            print("Unexpected recipe format")
            return
        
        self.process_recipe_details(recipe_name, recipe_data, matched_ingredients, substitutions, video_url)

    def process_recipe_details(self, recipe_name, recipe_data, matched_ingredients, substitutions, video_url):
        self.display.clear_details_frame()
        
        if recipe_name is None or recipe_data is None:
            print("Recipe name or data is missing")
            return
        self.populate_recipe_details_tasty(recipe_name, recipe_data, matched_ingredients, video_url)
        self.print_substitutions_tasty(substitutions)
        self.print_ingredients_and_instructions_tasty(recipe_name, recipe_data)
    
    def populate_recipe_details_bbc(self, recipe):
        self.clear_details_frame()
        self.display_recipe_name(recipe)
        self.display_recipe_url(recipe)
        self.display_matched_ingredients(recipe)
        self.display_ingredients_list(recipe)
        self.display_substitutions(recipe)
        self.display_instructions(recipe)
        self.display_preparation_and_cooking_time(recipe)

    def clear_details_frame(self):
        self.display.clear_details_frame()

    def display_recipe_name(self, recipe):
        tk.Label(
            self.display.details_container,
            text=recipe["name"],
            font=("Helvetica", 14, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")

    def display_recipe_url(self, recipe):
        tk.Label(
            self.display.details_container,
            text=f"URL: {recipe['url']}",
            anchor="w",
            bg="white",
            font=("Helvetica", 12),
        ).pack(fill="x")

    def display_matched_ingredients(self, recipe):
        matched_ingredients = recipe.get("matched_ingredients", [])
        matched_ingredients_text = f"Matched Ingredients: {len(matched_ingredients)}/{recipe.get('total_ingredients', 0)}"
        tk.Label(
            self.display.details_container,
            text=matched_ingredients_text,
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")
        for matched_ingredient in matched_ingredients:
            tk.Label(
                self.display.details_container,
                text=f"- {matched_ingredient}",
                anchor="w",
                bg="white",
                font=("Helvetica", 12),
            ).pack(fill="x")

    def display_ingredients_list(self, recipe):
        tk.Label(
            self.display.details_container,
            text="Ingredients:",
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")
        for ingredient in recipe.get("ingredients", []):
            tk.Label(
                self.display.details_container,
                text=f"- {ingredient}",
                anchor="w",
                bg="white",
                font=("Helvetica", 12),
            ).pack(fill="x")

    def display_substitutions(self, recipe):
        substitutions = recipe.get("substitutions", {})
        self.print_substitutions_bbc(substitutions)

    def display_instructions(self, recipe):
        tk.Label(
            self.display.details_container,
            text="Instructions:",
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")
        for step in recipe.get("steps", []):
            sentences = [sentence.strip() for sentence in step.split(". ") if sentence.strip()]
            for sentence in sentences:
                tk.Label(
                    self.display.details_container,
                    text=sentence,
                    font=("Helvetica", 12),
                    anchor="w",
                    bg="white",
                    justify="left",
                ).pack(fill="x")

    def display_preparation_and_cooking_time(self, recipe):
        prep_time = recipe.get("times", {}).get("Preparation", "N/A")
        cooking_time = recipe.get("times", {}).get("Cooking", "N/A")
        tk.Label(
            self.display.details_container,
            text=f"Preparation Time: {prep_time}",
            anchor="w",
            bg="white",
            font=("Helvetica", 12),
        ).pack(fill="x")
        tk.Label(
            self.display.details_container,
            text=f"Cooking Time: {cooking_time}",
            anchor="w",
            bg="white",
            font=("Helvetica", 12),
        ).pack(fill="x")
    
    def populate_recipe_details_tasty(
        self, recipe_name, recipe_data, matched_ingredients, video_url=None
    ):
        total_ingredients = sum(
            len(section.get("ingredients", []))
            for section in recipe_data.get("ingredient_sections", [])
        )
        matched_count = len(matched_ingredients)
        video_url = video_url = self.handler.video_db.get(
            self.handler.normalize_name(recipe_name)
        )

        tk.Label(
            self.display.details_container,
            text=f"Recipe Name: {recipe_name}",
            font=("Helvetica", 14, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")
        if video_url:
            tk.Label(
                self.display.details_container,
                text=f"Video URL: {video_url}",
                font=("Helvetica", 12),
                anchor="w",
                bg="white",
            ).pack(fill="x")

        tk.Label(
            self.display.details_container,
            text=f"Matched ingredients: ({matched_count}/{total_ingredients}):",
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")

        for matched_ingredient in matched_ingredients:
            tk.Label(
                self.display.details_container,
                text=f"- {matched_ingredient}",
                font=("Helvetica", 12),
                anchor="w",
                bg="white",
            ).pack(fill="x")


    def print_substitutions_bbc(self, substitutions):
        if substitutions:
            tk.Label(
                self.display.details_container,
                text="Substitutions for missing ingredients:",
                font=("Helvetica", 12, "bold"),
                anchor="w",
                bg="white",
            ).pack(fill="x")

            for ingredient, subs in substitutions.items():
                tk.Label(
                    self.display.details_container,
                    text=f"{ingredient.capitalize()}: {', '.join(subs)}",
                    font=("Helvetica", 12),
                    anchor="w",
                    bg="white",
                ).pack(fill="x")

    def print_ingredients_and_instructions_tasty(self, recipe_name, recipe_data):
        self.display_ingredients(recipe_data)
        self.display_instructions(recipe_data)

    def display_ingredients(self, recipe_data):
        tk.Label(
            self.display.details_container,
            text="Ingredients:",
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")
        for section in recipe_data.get("ingredient_sections", []):
            for ingredient_data in section.get("ingredients", []):
                self.pack_ingredient_label(ingredient_data)

    def pack_ingredient_label(self, ingredient_data):
        name = ingredient_data.get("name", "No name")
        primary_unit = ingredient_data.get("primary_unit", {})
        quantity = primary_unit.get("quantity") if primary_unit and "quantity" in primary_unit else ""
        display = primary_unit.get("display") if primary_unit and "display" in primary_unit else ""
        ingredient_parts = [part for part in [quantity, name, display] if part]
        ingredient_text = " - " + " ".join(ingredient_parts)
        tk.Label(
            self.display.details_container,
            text=ingredient_text,
            font=("Helvetica", 12),
            anchor="w",
            bg="white",
        ).pack(fill="x")

    def display_instructions(self, recipe_data):
        tk.Label(
            self.display.details_container,
            text="Instructions:",
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bg="white",
        ).pack(fill="x")
        for instruction in recipe_data.get("instructions", []):
            tk.Label(
                self.display.details_container,
                text=f" - {instruction['display_text']}",
                font=("Helvetica", 12),
                anchor="w",
                bg="white",
            ).pack(fill="x")

    def print_substitutions_tasty(self, substitutions):
        if any(substitutions.values()):
            tk.Label(
                self.display.details_container,
                text="Substitutions for missing ingredients:",
                font=("Helvetica", 12, "bold"),
                anchor="w",
                bg="white",
            ).pack(fill="x")
            for ingredient, subs in substitutions.items():
                if subs:
                    tk.Label(
                        self.display.details_container,
                        text=f"{ingredient.capitalize()}: {', '.join(subs)}",
                        font=("Helvetica", 12),
                        anchor="w",
                        bg="white",
                    ).pack(fill="x")