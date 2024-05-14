import tkinter as tk
from main_ui import MainUI
from models_tasty.tasty_parser import TastyParser
from search_ui import SearchUI


class AuthUI(MainUI):
    def __init__(self, root):
        super().__init__(root)
        self.tasty_parser = TastyParser()
        self.initial_ui_created = False
        self.create_initial_ui()

    def create_initial_ui(self):
        '''
        Initializes or refreshes the initial user interface for the application.

        Manages the setup of the button frame and account frame based on the UI's state.
        '''
        if not self.initial_ui_created:
            self.create_button_frame()
            self.account_frame = tk.Frame(self.root)
            self.add_initial_buttons()
            self.close_button()
            self.initial_ui_created = True
        else:
            self.clear_frame(self.account_frame)
            self.add_initial_buttons()
        self.inner_button_frame.pack(pady=20)
        self.button_frame.pack(expand=True)

    def create_account_frame(self):
        self.account_frame = tk.Frame(self.root)

    def add_field(self, frame, field_name, **kwargs):
        label = tk.Label(frame, text=field_name)
        label.pack(side=tk.TOP, pady=5)
        entry = tk.Entry(frame, **kwargs)
        entry.pack(side=tk.TOP, pady=5)
        return entry

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.root)
        self.inner_button_frame = tk.Frame(self.button_frame)
        self.inner_button_frame.pack(pady=20)

    def add_initial_buttons(self):
        '''
        Adds initial "Create account" and "Log in" buttons.

        Clears the current contents and sets up two primary buttons
        that lead to account creation and login functionalities.
        
        '''
        self.clear_frame(self.inner_button_frame)
        self.create_account_btn = tk.Button(
            self.inner_button_frame,
            text="Create account",
            command=self.show_account_creation_fields,
            width=20,
            height=2,
        )
        self.create_account_btn.pack(pady=10)
        self.login_btn = tk.Button(
            self.inner_button_frame,
            text="Log in",
            command=self.show_login_fields,
            width=20,
            height=2,
        )
        self.login_btn.pack(pady=10)

    def show_account_creation_fields(self):
        '''
        Displays the account creation fields in the UI.

        Clears the current buttons, adds a "Back" button,
        displays fields for username, password, and password confirmation for account creation.
        '''
        self.clear_frame(self.inner_button_frame)
        self.add_back_button()
        self.add_account_creation_fields()
        self.account_frame.pack(expand=True)

    def show_login_fields(self):
        '''
        Displays the login fields in the UI.

        Clears the current buttons of the inner button frame, adds a "Back" button,
        and displays fields for username and password entry for log in.
        '''
        
        self.clear_frame(self.inner_button_frame)
        self.add_back_button()
        self.add_login_fields()
        self.account_frame.pack(expand=True)

    def add_back_button(self):
        '''
        Adds a "Back" button to the inner button frame.

        Clears existing widgets before adding a new "Back" button.
        Triggers the `reset_ui` method, which restores the UI.
        '''
        self.clear_frame(self.inner_button_frame)
        back_btn = tk.Button(
            self.inner_button_frame,
            text="Back",
            command=self.reset_ui,
            width=20,
            height=2,
        )
        back_btn.pack(pady=10)

    def add_account_creation_fields(self):
        '''
        Creates fields for account creation in the UI.

        Sets up input fields for a username, password, and password confirmation within the account frame.
        A "Next" button is added below these fields, which triggers account creation when clicked.
        '''
        self.username_entry = self.add_field(self.account_frame, "Username")
        self.password_entry = self.add_field(self.account_frame, "Password", show="*")
        self.confirm_password_entry = self.add_field(
            self.account_frame, "Confirm Password", show="*"
        )
        next_btn = tk.Button(
            self.account_frame,
            text="Next",
            command=lambda: self.create_user(
                self.username_entry, self.password_entry, self.confirm_password_entry
            ),
        )
        next_btn.pack(pady=10)

    def add_login_fields(self):
        self.username_entry = self.add_field(self.account_frame, "Username")
        self.password_entry = self.add_field(self.account_frame, "Password", show="*")
        login_btn = tk.Button(
            self.account_frame,
            text="Log in",
            command=lambda: self.login_user(self.username_entry, self.password_entry),
        )
        login_btn.pack(pady=10)

    def close_button(self):
        close_btn = tk.Button(self.root, text="Close", command=self.root.quit)
        close_btn.place(
            relx=1.0, rely=1.0, x=-self.padding, y=-self.padding, anchor="se"
        )

    def reset_ui(self):
        self.clear_frame(self.account_frame)
        self.clear_frame(self.button_frame)
        self.inner_button_frame = tk.Frame(self.button_frame)
        self.add_initial_buttons()
        self.inner_button_frame.pack(pady=20)
        self.button_frame.pack(expand=True)

    def login_user(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()
        if super().login_user(username, password):
            self.transition_to_recipe_search()

    def transition_to_recipe_search(self):
        self.clear_window()
        SearchUI(self.root, self.tasty_parser)

    def clear_frame(self, frame):
        '''
        Clears all widgets from a specified frame.

        Destroys all child widgets contained within the frame to reset its state.
        '''
        for widget in frame.winfo_children():
            widget.destroy()

    def clear_window(self, keep_structure=False):
        '''
        Clears all widgets from the main application window.

        Reinitializes the basic UI structure if keep_structure is True.
        '''
        for widget in self.root.winfo_children():
            widget.destroy()
        if keep_structure:
            self.create_button_frame()
            self.create_account_frame()
