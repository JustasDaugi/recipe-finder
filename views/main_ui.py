from tkinter import messagebox
from users.user_data import User


class MainUI:
    def __init__(self, root):
        self.root = root
        self.user = User()
        self.padding = 10
        self.root.geometry("1500x600")

    def create_user(self, username_entry, password_entry, confirm_password_entry):
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if self.user.check_if_username_exists(username):
            messagebox.showerror("Error", "Username already exists")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            self.user.add_user(username, password)
            messagebox.showinfo(
                "Success", "Account created successfully. You can now log in."
            )

    def login_user(self, username, password):
        if self.user.check_login(username, password):
            self.user.save_current_user(username)
            return True
        else:
            messagebox.showerror("Failed", "Incorrect username or password.")
            return False
