import os
import json


class User:
    def __init__(self, base_dir="users"):
        self.user_data_file = os.path.join(base_dir, "user_data.json")
        self.current_user_file = os.path.join(base_dir, "current_user.json")

    def check_if_username_exists(self, username):
        try:
            with open(self.user_data_file, "r", encoding="utf-8") as file:
                users = json.load(file)
                return any(user["username"] == username for user in users)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def add_user(self, username, password):
        new_user = {"username": username, "password": password}
        users = []
        try:
            with open(self.user_data_file, "r", encoding="utf-8") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        users.append(new_user)
        with open(self.user_data_file, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)

    def check_login(self, username, password):
        try:
            with open(self.user_data_file, "r", encoding="utf-8") as file:
                users = json.load(file)
                return any(
                    user["username"] == username and user["password"] == password
                    for user in users
                )
        except FileNotFoundError:
            return False

    def save_current_user(self, username):
        user_data = {"username": username}
        with open(self.current_user_file, "w", encoding="utf-8") as file:
            json.dump(user_data, file, indent=4)

    def get_current_user(self):
        try:
            with open(self.current_user_file, "r", encoding="utf-8") as file:
                user_data = json.load(file)
                return user_data.get("username")
        except (FileNotFoundError, json.JSONDecodeError):
            return None
