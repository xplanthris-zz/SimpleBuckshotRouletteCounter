from tkinter import messagebox
import customtkinter as ctk
from SimpleBuckshotRouletteCounter import SimpleBuckshotRouletteCounter
from utils import check_admin_privileges
import keyboard, threading

def listen_for_keybinds(app):
    keyboard.add_hotkey('q', app.mark_live)
    keyboard.add_hotkey('e', app.mark_blank)
    keyboard.add_hotkey('z', app.new_round)
    keyboard.add_hotkey('f', app.use_burner_phone)
    keyboard.add_hotkey('t', app.use_polarizer)

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = SimpleBuckshotRouletteCounter(root)

    if not check_admin_privileges():
        messagebox.showwarning("Warning", "Please run this application with administrative privileges for keybinds to function properly.")
    else:
        threading.Thread(target=listen_for_keybinds, args=(app,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
