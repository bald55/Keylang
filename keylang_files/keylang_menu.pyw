import tkinter as tk
import os, sys
from tkinter import PhotoImage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from tkinter import filedialog
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OTHER_DIR = os.path.join(BASE_DIR, "other_stuff")
sys.path.insert(0, OTHER_DIR)

from keylang_editor import open_editor

import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

def button(text, command):
    return tk.Button(
        root,
        text=text,
        command=command,
        bg="#333",
        fg="#eee",
        activebackground="#80ef80",
        activeforeground="white",
        font=("Lato", 12, "italic", "bold"),
        relief="flat",
        borderwidth=0,
        padx=40,
        pady=20
    )

root = tk.Tk()
root.title("Keylang's awesome cool menu")
root.iconbitmap(os.path.join(BASE_DIR, "other_stuff", "Keylang_logo.ico"))
root.configure(bg="#1e1e1e")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

width = 1000
height = 700
x = (screen_width - width) // 2
y = (screen_height - height) // 2

root.geometry(f"{width}x{height}+{x}+{y}")

def new_script():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".kl",
        filetypes=[("Keylang files", "*.kl"), ("All files", "*.*")]
    )
    if filepath:
        print("Created:", filepath)
        with open(filepath, "w") as f:
            f.write("")
        open_editor(filepath)

def open_script():
    filepath = filedialog.askopenfilename(
        filetypes=[("Keylang files", "*.kl"), ("All files", "*.*")]
    )
    if filepath:
        print("Opened:", filepath)
        open_editor(filepath)

def quit_app():
    root.quit()

tk.Label(
    root,
    text="Keylang Script Editor",
    font=("Lato", 24, "bold"),
    fg="#80ef80",
    bg="#1e1e1e"
).pack(pady=(20, 10))
tk.Label(
    root,
    text="Best programming language!!!!",
    font=("Lato", 12, "bold"),
    fg="#ffffff",
    bg="#1e1e1e"
).pack(pady=(20, 10))


canvas = tk.Canvas(root, height=20, bg="#1e1e1e", highlightthickness=0)
canvas.pack(fill="x", pady=10)

width = 2500
for x in range(0, width, 15):
    canvas.create_line(x, 20, x+10, 0, fill="grey", width=3)


button("New Script", new_script).pack(pady=5)


canvas = tk.Canvas(root, height=20, bg="#1e1e1e", highlightthickness=0)
canvas.pack(fill="x", pady=10)

width = 2500
for x in range(0, width, 15):
    canvas.create_line(x, 20, x+10, 0, fill="grey", width=3)


logo_path = os.path.join(BASE_DIR, "other_stuff", "Keylang_logo.png")
logo_img = PhotoImage(file=logo_path)

smaller = logo_img.subsample(2, 2)

logo_label = tk.Label(root, image=smaller, bg="#1e1e1e")
logo_label.image = smaller

logo_label.place(relx=1.0, rely=0.65, anchor="e", x=-10)


button("Open Script", open_script).pack(pady=5)
button("Quit", quit_app).pack(pady=5)

bottom_label = tk.Label(root, text="version 2.0.0 (unstable)", font=("Lato", 10), fg="grey", bg="#1e1e1e")
bottom_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

link = tk.Label(root, text="Go to amazing website", font=("Lato", 12, "underline"), fg="#61afef", bg="#1e1e1e", cursor="hand2")
link.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
link.bind("<Button-1>", lambda e: webbrowser.open("https://bald55.github.io/keylang-site/"))

root.mainloop()