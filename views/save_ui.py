import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Text, END
from users.user_data import User
from models_tasty.tasty_parser import TastyParser
from models_tasty.tasty_handler import TastyHandler
from models_bbc.bbc_parser import BBCParser
from models_bbc.bbc_handler import BBCFileHandler



class SaveUI:
    def __init__(self, root, tasty_parser=None):
        self.root = root
        self.user = User()
        self.tasty_parser = TastyParser()
        self.bbc_parser = BBCParser()
        self.file_handler_bbc = BBCFileHandler("bbc.json", "subs.json")
        self.file_handler_tasty = TastyHandler("tasty.json", "url.json", "subs.json")
        self.selected_database = None
    
    def bbc_goodfood(self):
        self.selected_database = "bbc_goodfood"

    def tasty(self):
        self.selected_database = "tasty"
        if not self.tasty_parser:
            self.tasty_parser = TastyParser()

    def create_save_recipe_button(self):
        adjustment = 250
        middle_y_position = (600 // 2) - adjustment
        button_height = 30
        space_between_buttons = 30
        save_btn_y_position = middle_y_position - button_height - (space_between_buttons // 2)
        self.save_recipe_btn = tk.Button(
            self.root, text="Save recipe", command=self.toggle_save_recipe_entry
        )
        self.save_recipe_btn.place(x=10, y=save_btn_y_position, width=120)
        self.root.update_idletasks()
        view_saved_btn_x_position = self.save_recipe_btn.winfo_x()
        additional_space = 30
        view_saved_btn_y_position = save_btn_y_position + button_height + space_between_buttons + additional_space
        self.view_saved_recipes_btn = tk.Button(
            self.root, text="View saved recipes", command=self.view_saved_recipes_action
        )
        self.view_saved_recipes_btn.place(x=view_saved_btn_x_position, y=view_saved_btn_y_position, width=140)

        self.save_recipe_entry_visible = False

    def toggle_save_recipe_entry(self):
        btn_x, btn_y = self.save_recipe_btn.winfo_x(), self.save_recipe_btn.winfo_y()
        label_y = btn_y + self.save_recipe_btn.winfo_height() + 10
        entry_y = label_y + 20

        if not self.save_recipe_entry_visible:
            self.recipe_name_label = tk.Label(self.root, text="Recipe name: ")
            self.recipe_name_label.place(x=btn_x, y=label_y)

            self.save_recipe_entry = tk.Entry(self.root)
            self.save_recipe_entry.place(x=btn_x, y=entry_y, width=100)

            self.confirm_save_recipe_btn = tk.Button(
                self.root, text="Save", command=self.save_recipe_action
            )
            self.confirm_save_recipe_btn.place(x=btn_x + 105, y=entry_y, width=50)

            self.save_recipe_entry_visible = True
        else:
            self.recipe_name_label.place_forget()
            self.save_recipe_entry.place_forget()
            self.confirm_save_recipe_btn.place_forget()

            self.save_recipe_entry_visible = False
    
    def view_saved_recipes_action(self):
        username = self.user.get_current_user()
        bbc_recipes_str = self.get_bbc_recipes()
        tasty_recipes_str = self.get_tasty_recipes(username)
        combined_recipes_str = self.format_combined_recipes(bbc_recipes_str, tasty_recipes_str)
        self.display_recipe_window(combined_recipes_str)

    def get_bbc_recipes(self):
        return self.file_handler_bbc.view_saved_recipes() if self.bbc_parser else ""

    def get_tasty_recipes(self, username):
        return self.tasty_parser.get_saved_recipes_for_display(username) if self.tasty_parser else ""

    def format_combined_recipes(self, bbc_recipes_str, tasty_recipes_str):
        combined_recipes_str = ""
        if bbc_recipes_str.strip():
            combined_recipes_str += "BBC Goodfood recipes:" + bbc_recipes_str + "\n\n"
        if tasty_recipes_str.strip():
            combined_recipes_str += "Tasty recipes:\n" + tasty_recipes_str
        if not combined_recipes_str.strip():
            combined_recipes_str = "No saved recipes found."
        return combined_recipes_str

    def display_recipe_window(self, combined_recipes_str):
        recipe_window = Toplevel(self.root)
        recipe_window.title("Saved recipes")
        recipe_window.geometry("500x400")

        self.add_delete_recipe_entry(recipe_window)
        text_area, scrollbar = self.setup_text_area_and_scrollbar(recipe_window)
        text_area.insert(END, combined_recipes_str)
        text_area.config(state="disabled")

    def setup_text_area_and_scrollbar(self, window):
        text_area = Text(window, wrap="word", font=("Times New Roman", 12), bg="light gray")
        scrollbar = Scrollbar(window, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        text_area.pack(side="left", fill="both", expand=True)
        return text_area, scrollbar

    def add_delete_recipe_entry(self, parent_window):
        label = tk.Label(
            parent_window, text="Delete recipe", font=("Times New Roman", 12)
        )
        label.pack(pady=(10, 0))

        self.delete_recipe_entry = tk.Entry(parent_window, font=("Times New Roman", 12))
        self.delete_recipe_entry.pack(pady=10)

        delete_button = tk.Button(
            parent_window, text="Delete", command=self.delete_recipe_action
        )
        delete_button.pack(pady=(0, 10))

    def save_recipe_action(self):
        """Initiates the process of saving a recipe after validating input and the selected database."""
        recipe_name = self.get_recipe_name()
        if not recipe_name:
            return  # Error message from method

        if not self.validate_database_selection():
            return  # Error message from method

        save_message = self.process_recipe_saving(recipe_name)
        if save_message:
            messagebox.showinfo("Success", save_message)
            self.reset_save_recipe_widgets()

    def get_recipe_name(self):
        """Retrieves and validates the recipe name from the entry widget."""
        recipe_name = self.save_recipe_entry.get().strip()
        if not recipe_name:
            messagebox.showerror("Error", "Please enter a recipe name.")
        return recipe_name

    def validate_database_selection(self):
        """Checks if a database is selected and shows an error message if not."""
        if self.selected_database is None:
            messagebox.showinfo(
                "Select database", "Please select a database before saving a recipe."
            )
            return False
        return True

    def process_recipe_saving(self, recipe_name):
        """Handles fetching and saving a recipe from the selected database."""
        if self.selected_database == "bbc_goodfood":
            return self.save_recipe_bbc(recipe_name)
        elif self.selected_database == "tasty":
            return self.save_recipe_tasty(recipe_name)
        else:
            messagebox.showerror("Error", "No database selected.")
            return None

    def save_recipe_bbc(self, recipe_name):
        """Fetches and saves a BBC Goodfood recipe."""
        recipe_data = self.bbc_parser.search_recipe_by_name(recipe_name)
        if "message" in recipe_data:
            messagebox.showerror("Error", recipe_data["message"])
            return None
        return self.file_handler_bbc.save_recipe_to_file(recipe_data)

    def save_recipe_tasty(self, recipe_name):
        """Fetches and saves a Tasty recipe."""
        recipe_data = self.tasty_parser.search_recipe_by_name_tasty(recipe_name)
        if "message" in recipe_data:
            messagebox.showerror("Error", recipe_data["message"])
            return None
        return self.file_handler_tasty.save_recipe_to_file_tasty(recipe_data["name"])

    def delete_recipe_action(self):
        recipe_name = self.delete_recipe_entry.get().strip()
        if not recipe_name:
            messagebox.showinfo("Result", "Please enter a recipe name to delete.")
            return

        if self.selected_database == "bbc_goodfood":
            delete_bbc = self.file_handler_bbc.delete_recipe_by_name(recipe_name)
            messagebox.showinfo("Result", delete_bbc)
        elif self.selected_database == "tasty":
            delete_tasty = self.file_handler_tasty.delete_recipe_by_name_tasty(recipe_name)
            messagebox.showinfo("Result", delete_tasty)
        else:
            messagebox.showinfo("Result", "Please select a database before attempting to delete a recipe.")

    def reset_save_recipe_widgets(self):
        self.recipe_name_label.place_forget()
        self.save_recipe_entry.place_forget()
        self.confirm_save_recipe_btn.place_forget()
        self.save_recipe_entry_visible = False
