import unittest
import os
import json
import tempfile
from users.user_data import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir.name
        self.user = User(base_dir=self.base_dir)
        os.makedirs(os.path.join(self.base_dir, "users"), exist_ok=True)
        user_data_file = os.path.join(self.base_dir, "users", "user_data.json")
        with open(user_data_file, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
        current_user_file = os.path.join(self.base_dir, "users", "current_user.json")
        with open(current_user_file, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_check_if_username_exists(self):
        self.user.add_user("testuser", "testpassword")
        self.assertTrue(self.user.check_if_username_exists("testuser"))
        self.assertFalse(self.user.check_if_username_exists("nonexistentuser"))

    def test_check_login(self):
        self.user.add_user("testuser", "testpassword")
        self.assertTrue(self.user.check_login("testuser", "testpassword"))
        self.assertFalse(self.user.check_login("testuser", "wrongpassword"))
        self.assertFalse(self.user.check_login("nonexistentuser", "testpassword"))


if __name__ == '__main__':
    unittest.main()

