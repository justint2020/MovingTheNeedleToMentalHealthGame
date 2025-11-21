import tkinter as tk
import subprocess
import sys
import os

def set_difficulty(level):
    if level == "Easy":
        os.environ["GAME_DIFFICULTY"] = "Easy"
    elif level == "Normal":
        os.environ["GAME_DIFFICULTY"] = "Normal"
    elif level == "Hard":
        os.environ["GAME_DIFFICULTY"] = "Hard"

def back_to_menu():
    script_path = os.path.join(os.path.dirname(__file__), "StartMenu.py")
    subprocess.Popen([sys.executable, script_path])
    root.destroy()

root = tk.Tk()
root.title("Settings")
root.geometry("400x350")

title_label = tk.Label(root, text="Settings", font=("Arial", 24))
title_label.pack(pady=20)

easy_btn = tk.Button(root, text="Easy", font=("Arial", 16), width=15,
                     command=lambda: set_difficulty("Easy"))
easy_btn.pack(pady=5)

normal_btn = tk.Button(root, text="Normal", font=("Arial", 16), width=15,
                       command=lambda: set_difficulty("Normal"))
normal_btn.pack(pady=5)

hard_btn = tk.Button(root, text="Hard", font=("Arial", 16), width=15,
                     command=lambda: set_difficulty("Hard"))
hard_btn.pack(pady=5)

label = tk.Label(root, text="Adjust so experience can be a growth zone.", font=("Arial", 12))
label.pack(pady=20)

back_button = tk.Button(root, text="Back to Main Menu", font=("Arial", 14),
                        width=20, command=back_to_menu)
back_button.pack(pady=10)

root.mainloop()
