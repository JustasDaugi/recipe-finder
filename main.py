import tkinter as tk
import sys
import os

# This block seems to have fixed the import issues
current_dir = os.path.dirname(__file__)
ui_dir = os.path.join(current_dir, 'views')
if ui_dir not in sys.path:
    sys.path.insert(0, ui_dir)
from views.auth_ui import AuthUI


def main():
    
    root = tk.Tk()
    AuthUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# import os
# print (os.getcwd())