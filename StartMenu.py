import tkinter as tk
import subprocess
import sys
import os

def start_game():
    script_path = os.path.join(os.path.dirname(__file__), "TheGame.py")
    subprocess.Popen([sys.executable, script_path], env=os.environ)
    root.destroy()

def open_info():
    script_path = os.path.join(os.path.dirname(__file__), "info.py")
    subprocess.Popen([sys.executable, script_path])
    root.destroy()

def open_settings():
    script_path = os.path.join(os.path.dirname(__file__), "settings.py")
    subprocess.Popen([sys.executable, script_path])
    root.destroy()

root = tk.Tk()
root.title("Start Menu")
root.geometry("400x350")

title_label = tk.Label(root, text="Start Menu", font=("Arial", 24))
title_label.pack(pady=30)

play_button = tk.Button(root, text="Play", font=("Arial", 16),
                        width=15, command=start_game)
play_button.pack(pady=10)

info_button = tk.Button(root, text="Information", font=("Arial", 16),
                        width=15, command=open_info)
info_button.pack(pady=10)

settings_button = tk.Button(root, text="Settings", font=("Arial", 16),
                            width=15, command=open_settings)
settings_button.pack(pady=10)

quit_button = tk.Button(root, text="Quit", font=("Arial", 16),
                        width=15, command=root.destroy)
quit_button.pack(pady=10)

root.mainloop()
