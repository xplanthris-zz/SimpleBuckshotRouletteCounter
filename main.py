# TODO: Version 2.0.0 baby

from tkinter import messagebox
from utils import check_admin_privileges
import customtkinter as ctk
from SimpleBuckshotRouletteCounter import SimpleBuckshotRouletteCounter

def main():
    if not check_admin_privileges():
        messagebox.showwarning("Warning", "Please run this application with administrative privileges for keybinds to function properly.")
    
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = SimpleBuckshotRouletteCounter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
