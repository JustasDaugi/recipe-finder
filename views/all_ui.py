import tkinter as tk
from tkinter import Toplevel
from models_tasty.tasty_handler import TastyHandler
from models_bbc.bbc_handler import BBCFileHandler

class AllRecipeUI:
    def __init__(self, root):
        self.root = root
        self.file_handler_tasty = TastyHandler("tasty.json", "url.json", "subs.json")
        self.file_handler_bbc = BBCFileHandler("bbc.json", "subs.json")
        
    def create_view_recipes_buttons(self):
        button_x_position = 10
        button_y_position_bbc = 150
        button_y_position_tasty = 180
        button_width = 180
        self.view_bbc_recipes_btn = tk.Button(
            self.root,
            text="View all BBC Good Food recipes",
            command=self.display_bbc_recipes,
        )
        self.view_bbc_recipes_btn.place(
            x=button_x_position, y=button_y_position_bbc, width=button_width
        )

        self.view_tasty_recipes_btn = tk.Button(
            self.root,
            text="View all Tasty recipes",
            command=self.display_tasty_recipes,
        )
        self.view_tasty_recipes_btn.place(
            x=button_x_position, y=button_y_position_tasty, width=button_width
        )

    def display_bbc_recipes(self):
        self.selected_database = "bbc_goodfood"
        bbc_recipes = self.file_handler_bbc.load_bbc_recipes()
        # Stores recipes in a class instance
        self.recipes = bbc_recipes
        self.create_recipe_display_window(bbc_recipes, "BBC Good Food")

    def display_tasty_recipes(self):
        self.selected_database = "tasty"
        tasty_recipes = self.file_handler_tasty.load_tasty_recipes()
        self.recipes = tasty_recipes
        self.create_recipe_display_window(tasty_recipes, "Tasty")
        
    def create_recipe_display_window(self, recipes, source):
        recipe_window = Toplevel(self.root)
        recipe_window.title(f"{source} Recipes")

        search_container = tk.Frame(recipe_window)
        search_container.pack(fill="x", padx=10, pady=5)

        search_label = tk.Label(search_container, text="Search recipe by name:")
        search_label.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_container)
        search_entry.pack(side=tk.LEFT, padx=(5, 0), fill="x", expand=True)

        listbox_frame = tk.Frame(recipe_window)
        listbox_frame.pack(fill="both", expand=True, pady=(0, 10))

        names_listbox = tk.Listbox(listbox_frame, width=40, height=20)
        names_listbox.pack(side="left", fill="y")

        names_scrollbar = tk.Scrollbar(
            listbox_frame, orient="vertical", command=names_listbox.yview
        )
        names_scrollbar.pack(side="left", fill="y")
        names_listbox.config(yscrollcommand=names_scrollbar.set)

        details_text = tk.Text(
            listbox_frame, wrap="word", width=80, height=20, state="disabled"
        )
        details_text.pack(side="left", fill="both", expand=True)

        filtered_recipes = []

        def filter_recipes(event=None):
            """
            Filters recipes based on a user's search query and updates the listbox.

            This function is triggered by a key release event in the search entry widget.

            Parameters:
                event (Event, optional): The event that triggered this callback. Defaults to None.
            """
            # Referencing the list in create_recipe_display_window
            nonlocal filtered_recipes
            search_query = search_entry.get().strip().lower()
            filtered_recipes = [
                recipe
                for recipe in recipes
                if search_query in recipe.get("name", "No Name").lower()
            ]
            names_listbox.delete(0, tk.END)
            for recipe in filtered_recipes:
                names_listbox.insert(tk.END, recipe.get("name", "No Name"))

        def on_recipe_selected(event):
            """
            Displays details of the selected recipe in the text widget.

            Retrieves the selected recipe's details and displays them in a text widget.

            Parameters:
                event : The event that contains information about the listbox selection.
            """
            # Check which recipe has been selected by the user in the listbox
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                selected_recipe = filtered_recipes[index]
                details_text.config(state="normal")
                details_text.delete(1.0, tk.END)
                if source == "BBC Good Food":
                    details_text.insert(
                        tk.END, f"Name: {selected_recipe.get('name', 'No Name')}\n"
                    )
                    details_text.insert(
                        tk.END, f"URL: {selected_recipe.get('url', 'No URL')}\n\n"
                    )
                    details_text.insert(tk.END, "Ingredients:\n")
                    for ingredient in selected_recipe.get("ingredients", []):
                        details_text.insert(tk.END, f"- {ingredient}\n")
                    details_text.insert(tk.END, "\nSteps:\n")
                    for step in selected_recipe.get("steps", []):
                        details_text.insert(tk.END, f"{step}\n")
                elif source == "Tasty":
                    self.print_ingredients_and_instructions_tasty(
                        selected_recipe, details_text
                    )
                details_text.config(state="disabled")

        search_entry.bind("<KeyRelease>", filter_recipes)
        names_listbox.bind("<<ListboxSelect>>", on_recipe_selected)

        filter_recipes()

    def print_ingredients_and_instructions_tasty(self, recipe, details_text_widget):
        recipe_name = recipe.get("name", "No Name")
        video_url = self.file_handler_tasty.video_db.get(
            self.file_handler_tasty.normalize_name(recipe_name), "URL not available"
        )

        details_text_widget.insert(tk.END, f"Name: {recipe_name}\n")
        details_text_widget.insert(tk.END, f"URL: {video_url}\n\n")

        details_text_widget.insert(tk.END, "Ingredients:\n")
        for section in recipe.get("ingredient_sections", []):
            for ingredient_data in section.get("ingredients", []):
                name = ingredient_data.get("name", "No name")
                primary_unit = ingredient_data.get("primary_unit", {})
                quantity = primary_unit.get("quantity", "")
                display = primary_unit.get("display", "")
                ingredient_parts = [part for part in [quantity, display, name] if part]
                ingredient_text = " - " + " ".join(ingredient_parts) + "\n"
                details_text_widget.insert(tk.END, ingredient_text)

        details_text_widget.insert(tk.END, "\nInstructions:\n")
        for instruction in recipe.get("instructions", []):
            instruction_text = instruction.get("display_text", "No instruction")
            details_text_widget.insert(tk.END, f"- {instruction_text}\n")

