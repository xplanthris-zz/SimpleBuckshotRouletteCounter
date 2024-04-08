# Standard library imports
import threading

# Third-party imports
from tkinter import messagebox
import customtkinter as ctk
import keyboard

# Local application imports
from SimpleBuckshotRouletteCounter import SimpleBuckshotRouletteCounter
from utils import check_admin_privileges


def listen_for_keybinds(app):
    """
    Sets up hotkeys for the application.

    Args:
    app: The main application instance.
    """
    keyboard.add_hotkey("q", app.mark_live)
    keyboard.add_hotkey("e", app.mark_blank)
    keyboard.add_hotkey("z", app.new_round)
    keyboard.add_hotkey("f", app.use_burner_phone)
    keyboard.add_hotkey("t", app.use_polarizer)


def main():
    """
    The main function to run the application.
    """
    # Setting up the application's appearance and theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Initializing the main window and application
    root = ctk.CTk()
    app = SimpleBuckshotRouletteCounter(root)

    # Check for admin privileges for keybind functionality
    if not check_admin_privileges():
        messagebox.showwarning(
            "Warning",
            "Please run this application with administrative privileges for keybinds to function properly.",
        )
    else:
        # Starting a thread to listen for keybinds
        threading.Thread(target=listen_for_keybinds, args=(app,), daemon=True).start()

    # Running the main application loop
    root.mainloop()


# Entry point of the script
if __name__ == "__main__":
    main()
