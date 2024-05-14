from main_ui import MainUI
from users.user_data import User 
import tkinter as tk
from all_ui import AllRecipeUI
from models_tasty.tasty_parser import TastyParser
from models_bbc.bbc_parser import BBCParser
from models_tasty.tasty_handler import TastyHandler
from details_ui import DetailsUI
from save_ui import SaveUI


class SearchUI(MainUI):
    def __init__(self, root, tasty_parser=None):
        # Refering to super class MainUI, which contains the main window parameters
        super().__init__(root)
        self.recipes = []
        self.selected_database = None
        self.bbc_parser = BBCParser()
        self.tasty_parser = TastyParser()
        self.user = User()
        self.save_ui = SaveUI(root)
        self.all_recipes = AllRecipeUI(root)
        self.setup_search_ui()
        self.create_details_frame()
        self.save_ui.create_save_recipe_button()
        self.all_recipes.create_view_recipes_buttons()

    def setup_search_ui(self):
        self.display_recipe_search_fields()

    def create_details_frame(self):
        self.details_frame = tk.Frame(
            self.root, width=300, bg="white", bd=2, relief="groove"
        )
        self.details_frame.pack(
            fill="both", expand=True, side="right", padx=10, pady=10
        )
        self.details_frame.pack_propagate(False)
        self.setup_details_canvas()

    def display_recipe_search_fields(self):
        """Sets up the UI for recipe search with various components."""
        self.views = DetailsUI(self.root, self)
        self.clear_window()
        self.create_back_button_frame()
        self.save_ui.create_save_recipe_button()
        
        container = self.setup_container()
        self.add_find_recipe_label(container)
        self.add_database_selection_ui(container)
        self.add_ingredient_entry_fields(container)
        self.add_search_button(container)
        self.add_results_display(container)

    def setup_container(self):
        """Create and return the main container frame for the search fields."""
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10, side="left")
        return container

    def add_find_recipe_label(self, container):
        """Add the main label for the recipe search section."""
        find_recipe_label = tk.Label(
            container, text="Find a Recipe", font=("Helvetica", 16, "bold")
        )
        find_recipe_label.pack(pady=(10, 20))

    def add_database_selection_ui(self, container):
        """Add UI components for database selection."""
        database_select = tk.Label(
            container, text="Select a database to find recipes: "
        )
        database_select.pack(pady=(0, 0))

        source_buttons_frame = tk.Frame(container)
        source_buttons_frame.pack(pady=(10, 0))
        self.selected_source = tk.StringVar(value="none")
        self.add_radio_buttons(source_buttons_frame)

    def add_radio_buttons(self, frame):
        """Add radio buttons for selecting the source database."""
        bbc_goodfood_radio = tk.Radiobutton(
            frame,
            text="BBC Good Food",
            variable=self.selected_source,
            value="BBC Good Food",
            command=self.save_ui.bbc_goodfood,
        )
        bbc_goodfood_radio.pack(side=tk.LEFT, padx=(0, 10))

        tasty_radio = tk.Radiobutton(
            frame,
            text="Tasty",
            variable=self.selected_source,
            value="Tasty",
            command=self.save_ui.tasty,
        )
        tasty_radio.pack(side=tk.LEFT)

    def add_ingredient_entry_fields(self, container):
        """Add entry fields for ingredients and spices."""
        ingredients_label = tk.Label(
            container,
            text="Enter your ingredients - vegetables, meats, grains, dairy products etc.",
        )
        ingredients_label.pack(pady=(5, 0))

        self.ingredient_input_entry = tk.Entry(container)
        self.ingredient_input_entry.pack(pady=(0, 5))

        spices_label = tk.Label(container, text="Enter spices, condiments etc.")
        spices_label.pack(pady=(0, 0))

        self.spice_input_entry = tk.Entry(container)
        self.spice_input_entry.pack(pady=5)

    def add_search_button(self, container):
        """Add the search button."""
        search_btn = tk.Button(
            container, text="Search", command=self.handle_recipe_search
        )
        search_btn.pack(pady=10)

    def add_results_display(self, container):
        """Setup the listbox and scrollbar for displaying search results."""
        results_frame = tk.Frame(container)
        results_frame.pack(fill="both", expand=True)
        self.result_listbox = tk.Listbox(results_frame, width=1, height=15)
        self.result_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(
            results_frame, orient="vertical", command=self.result_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.result_listbox.config(yscrollcommand=scrollbar.set)
        self.result_listbox.bind("<<ListboxSelect>>", self.views.on_recipe_selected)

    def create_back_button_frame(self):
        self.back_button_frame = tk.Frame(self.root)
        self.back_button_frame.pack(fill="x", pady=10)
        back_btn = tk.Button(
            self.back_button_frame, text="Back", command=self.reset_to_initial_ui
        )
        back_btn.pack()

    def clear_details_frame(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.setup_details_canvas()

    def setup_details_canvas(self):
        '''
        Sets up a canvas with vertical and horizontal scrollbars in the details frame. 
        Canvas displays a container frame for additional UI components.
        '''        
        
        self.details_canvas = tk.Canvas(self.details_frame, bg="white")
        self.vertical_scrollbar = tk.Scrollbar(
            self.details_frame, orient="vertical", command=self.details_canvas.yview
        )
        self.horizontal_scrollbar = tk.Scrollbar(
            self.details_frame, orient="horizontal", command=self.details_canvas.xview
        )
        self.details_canvas.configure(
            yscrollcommand=self.vertical_scrollbar.set,
            xscrollcommand=self.horizontal_scrollbar.set,
        )
        self.vertical_scrollbar.pack(side="right", fill="y")
        self.horizontal_scrollbar.pack(side="bottom", fill="x")
        self.details_canvas.pack(side="left", fill="both", expand=True)
        self.details_container = tk.Frame(self.details_canvas, bg="white")
        self.details_canvas.create_window(
            (0, 0), window=self.details_container, anchor="nw"
        )
        self.details_container.bind(
            "<Configure>",
            lambda e: self.details_canvas.configure(
                scrollregion=self.details_canvas.bbox("all")
            ),
        )

    def handle_recipe_search(self):
        '''
        Handles the recipe search based on the selected database.

        Checks for database selection and initializes parsers. 
        Retrieves user input for ingredients and spices, processes them and displays matching recipes.
        '''
        
        if not self.is_database_selected():
            self.show_database_selection_required_message()
            return

        database_type = self.save_ui.selected_database.lower()
        if database_type == "tasty":
            self.process_search_tasty()
        elif database_type == "bbc_goodfood":
            self.process_search_bbc_goodfood()
        else:
            print("No database selected.")

    def is_database_selected(self):
        return hasattr(self.save_ui, 'selected_database') and self.save_ui.selected_database is not None

    def show_database_selection_required_message(self):
        tk.messagebox.showinfo("Database Selection Required", "Please select a database first.")

    def process_search_tasty(self):
        if not hasattr(self, 'tasty_parser'):
            self.tasty_parser = TastyParser()

        food_input, spice_input = self.get_ingredients_input()
        user_ingredients = self.tasty_parser.parse_ingredients(food_input, spice_input)

        if user_ingredients is False:
            self.show_invalid_format_message("dot")
            return

        self.clear_and_display_results_tasty(user_ingredients)

    def process_search_bbc_goodfood(self):
        if not hasattr(self, 'bbc_parser'):
            self.bbc_parser = BBCParser()

        food_input, spice_input = self.get_ingredients_input()
        user_ingredients = self.bbc_parser.parse_ingredients(food_input, spice_input)

        if user_ingredients is False:
            self.show_invalid_format_message("comma and space")
            return

        self.clear_and_display_results_bbc(user_ingredients)

    def get_ingredients_input(self):
        food_input = self.ingredient_input_entry.get()
        spice_input = self.spice_input_entry.get()
        return food_input, spice_input

    def show_invalid_format_message(self, separator):
        message = f"Invalid input format. Ingredients have to be separated by a {separator}."
        tk.messagebox.showinfo("Invalid Input Format", message)

    def clear_and_display_results_tasty(self, user_ingredients):
        ''' Clears and displays results using the TastyParser '''
        matches = self.tasty_parser.find_matching_recipes(user_ingredients)
        self.result_listbox.delete(0, tk.END)
        self.recipes = []
        for match in matches:
            self.result_listbox.insert(tk.END, match[0])
            self.recipes.append(match)

    def clear_and_display_results_bbc(self, user_ingredients):
        ''' Clears and displays results using the BBCParser '''
        matches = self.bbc_parser.find_matching_recipes(user_ingredients)
        self.result_listbox.delete(0, tk.END)
        self.recipes = matches
        for recipe in matches:
            self.result_listbox.insert(tk.END, recipe["name"])

    def reset_to_initial_ui(self):
        from auth_ui import AuthUI

        self.clear_window()
        login_instance = AuthUI(self.root)
        login_instance.create_initial_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    display_instance = SearchUI(root)
    views_instance = DetailsUI(root, display_instance)
    finder = TastyHandler("tasty.json", "dishes.json", "subs.json")
    matcher = TastyParser()
    root.mainloop()
