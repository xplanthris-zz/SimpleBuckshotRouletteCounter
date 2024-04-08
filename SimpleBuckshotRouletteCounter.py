from tkinter import simpledialog, messagebox
import customtkinter as ctk

from Bullet import Bullet


class SimpleBuckshotRouletteCounter:
    """A GUI application to track rounds for Buckshot Roulette"""

    def __init__(self, master):
        """Initialize the main application window and widgets."""
        self.master = master
        self.setup_ui()

        self.live = 0  # Counter for live bullets
        self.blank = 0  # Counter for blank bullets
        self.bullets = []  # List to track the status of each bullet
        self.current_bullet_index = 0  # Index to keep track of the current bullet

    def setup_ui(self):
        """Configure UI components and layout."""
        self.master.title("SimpleBuckshotRouletteCounter")
        self.master.resizable(width=False, height=False)
        self.master.geometry("400x128")
        self.master.attributes("-topmost", True)

        # Labels for live and blank bullets
        self.live_label = ctk.CTkLabel(self.master, text="Live: 0 (0%)")
        self.live_label.grid(row=1, column=0, pady=(10, 0), padx=10)
        self.blank_label = ctk.CTkLabel(self.master, text="Blank: 0 (0%)")
        self.blank_label.grid(row=1, column=2, pady=(10, 0), padx=10)

        # Buttons for marking bullets and using game tools
        self.live_button = ctk.CTkButton(
            self.master,
            text="Live",
            command=lambda: self.mark_bullet(Bullet.LIVE),
            fg_color="red",
        )
        self.live_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.blank_button = ctk.CTkButton(
            self.master,
            text="Blank",
            command=lambda: self.mark_bullet(Bullet.BLANK),
            fg_color="blue",
        )
        self.blank_button.grid(row=2, column=2, sticky="ew", padx=5, pady=5)
        self.new_round_button = ctk.CTkButton(
            self.master, text="New Round", command=self.new_round, fg_color="grey"
        )
        self.new_round_button.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.polarizer_button = ctk.CTkButton(
            self.master, text="Polarizer", command=self.use_polarizer, fg_color="grey"
        )
        self.polarizer_button.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        self.burner_phone_button = ctk.CTkButton(
            self.master,
            text="Burner Phone",
            command=self.use_burner_phone,
            fg_color="grey",
        )
        self.burner_phone_button.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

        # Configure column weights for equal button width
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

    # Simplified bullet marking methods
    def mark_live(self):
        """Marks the current bullet as live."""
        self.mark_bullet(Bullet.LIVE)

    def mark_blank(self):
        """Marks the current bullet as blank."""
        self.mark_bullet(Bullet.BLANK)

    # New round setup with user input for bullet count and distribution
    def new_round(self):
        """Starts a new round with user-defined bullet settings."""
        try:
            # Asking the user for the total number of bullets
            total_bullets = simpledialog.askinteger(
                "New Round",
                "How many bullets are there?",
                parent=self.master,
                minvalue=2,
                maxvalue=8,
            )
            if total_bullets is None:
                return

            # Handling odd number of bullets to determine extra live or blank
            if total_bullets % 2 != 0:
                more_what = simpledialog.askstring(
                    "New Round", "Is there more (L)ive's or (B)lank's?"
                )
                if more_what is None:
                    return

                live, blank = (
                    (total_bullets - blank, blank)
                    if more_what.strip().upper() in ["L", "LIVE"]
                    else (total_bullets // 2, total_bullets // 2)
                )
            else:
                live = blank = total_bullets // 2

            # Initializing bullet tracking
            self.bullets = [Bullet.UNKNOWN] * total_bullets
            self.live = live
            self.blank = blank
            self.current_bullet_index = 0

            self.update_labels()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Invalid input or error occurred: {e}. Please try again."
            )

    # Marking bullets and handling autofill logic
    def mark_bullet(self, bullet_type):
        """Marks the current bullet and automatically proceeds to the next."""
        if (
            self.current_bullet_index < len(self.bullets)
            and self.bullets[self.current_bullet_index] is Bullet.UNKNOWN
        ):
            self.bullets[self.current_bullet_index] = bullet_type
            if bullet_type == Bullet.LIVE and self.live > 0:
                self.live -= 1
            elif bullet_type == Bullet.BLANK and self.blank > 0:
                self.blank -= 1

            self.autofill_check()
            self.update_labels()

        self.proceed_to_next_bullet()

    # Proceed to the next bullet, automatically skipping known bullets
    def proceed_to_next_bullet(self):
        """Moves to the next bullet, handling already marked bullets."""
        self.current_bullet_index += 1
        if self.current_bullet_index < len(self.bullets):
            if self.bullets[self.current_bullet_index] is not Bullet.UNKNOWN:
                bullet_type = self.bullets[self.current_bullet_index]
                bullet_description = (
                    "live"
                    if bullet_type in [Bullet.LIVE, Bullet.LIVE_MARKED]
                    else "blank"
                )
                messagebox.showinfo(
                    "Bullet Predetermined", f"This bullet is a {bullet_description}."
                )
                self.live -= 1 if bullet_description == "live" else 0
                self.blank -= 1 if bullet_description == "blank" else 0
                self.bullets[self.current_bullet_index] = (
                    Bullet.LIVE if bullet_description == "live" else Bullet.BLANK
                )
                self.update_labels()
                self.proceed_to_next_bullet()
        else:
            messagebox.showinfo(
                "Round Complete", "This round has ended. Starting a new round."
            )
            self.new_round()

    # Updating the UI labels to reflect current bullet counts
    def update_labels(self):
        """Updates the UI labels with the current count and percentage of live and blank bullets."""
        total_bullets = self.live + self.blank
        live_percent = self.live / total_bullets * 100 if total_bullets > 0 else 0
        blank_percent = self.blank / total_bullets * 100 if total_bullets > 0 else 0
        self.live_label.configure(text=f"Live: {self.live} ({live_percent:.2f}%)")
        self.blank_label.configure(text=f"Blank: {self.blank} ({blank_percent:.2f}%)")

    # Using the Burner Phone feature
    def use_burner_phone(self):
        """Allows the user to mark a bullet at a specific position as live or blank."""
        if self.current_bullet_index < len(self.bullets):
            position = (
                simpledialog.askinteger(
                    "Burner Phone",
                    "Enter the bullet position (1-indexed):",
                    parent=self.master,
                )
                - 1
            )
            if position is None or not 0 <= position < len(self.bullets):
                messagebox.showerror("Error", "Invalid bullet position.")
                return

            bullet_type_input = simpledialog.askstring(
                "Burner Phone",
                "Enter the bullet type (L)ive or (B)lank:",
                parent=self.master,
            )
            if bullet_type_input is None or bullet_type_input.strip().upper() not in [
                "L",
                "B",
                "LIVE",
                "BLANK",
            ]:
                messagebox.showerror(
                    "Error", "Invalid bullet type. Please enter 'Live' or 'Blank'."
                )
                return

            bullet_type = (
                Bullet.LIVE_MARKED
                if bullet_type_input in ["L", "LIVE"]
                else Bullet.BLANK_MARKED
            )
            self.bullets[position] = bullet_type
            self.autofill_check()
            self.update_labels()
            messagebox.showinfo(
                "Burner Phone",
                f"The bullet at position {position + 1} is marked as {'live' if bullet_type == Bullet.LIVE_MARKED else 'blank'}.",
            )
        else:
            self.new_round()

    def use_polarizer(self):
        """Uses the polarizer tool to invert the bullet type at the current index."""
        if self.current_bullet_index < len(self.bullets):
            current_bullet = self.bullets[self.current_bullet_index]
            # If the bullet is already marked with the polarizer (LIVE_MARKED or BLANK_MARKED)
            if current_bullet in [Bullet.LIVE_MARKED, Bullet.BLANK_MARKED]:
                # Adjust counts based on the marked type
                self.live -= 1 if current_bullet == Bullet.LIVE_MARKED else 0
                self.blank -= 1 if current_bullet == Bullet.BLANK_MARKED else 0
            else:
                # Ask user for the new bullet type after polarization
                bullet_type = simpledialog.askstring(
                    "Polarizer", "What was the bullet inverted to? (L)ive or (B)lank?"
                )
                if bullet_type is None or bullet_type.strip().upper() not in [
                    "L",
                    "LIVE",
                    "B",
                    "BLANK",
                ]:
                    messagebox.showerror("Invalid Input", "Please enter a valid type")
                    return

                # Adjust counts based on user input
                if bullet_type.strip().upper() in ["L", "LIVE"]:
                    self.blank -= 1
                else:
                    self.live -= 1

            self.update_labels()
            self.current_bullet_index += 1

    def autofill_check(self):
        # Since this is the most complicated part of the code, I'll explain
        # We have 2 cases
        # 1. Fill case, [Live, Live, None, None] 2 blanks, this is an easy fill
        # 2. The harder more gut wrenching case, gap cases, [Live, Live, None, Live, None] now technically we have 1 live and 2 blanks but we cannot just fill it like that so instead what we did was bullets marked by the burner phone are marked as LM or BM so we count the *M(s)
        # and now IF the amount of *M unit subtracted by the L / B unit = 0 this means ok there is only this we fill all None(s)
        # - xplanthris sunday apr 7 8:09 pm
        if self.live == 0 and self.blank != 0:
            for i in range(len(self.bullets)):
                if self.bullets[i] is Bullet.UNKNOWN:
                    self.bullets[i] = Bullet.BLANK
        elif self.blank == 0 and self.live != 0:
            for i in range(len(self.bullets)):
                if self.bullets[i] is Bullet.UNKNOWN:
                    self.bullets[i] = Bullet.LIVE
        else:
            if (
                self.bullets.count(Bullet.BLANK_MARKED) != 0
                and self.bullets.count(Bullet.LIVE_MARKED) == 0
                and self.blank - self.bullets.count(Bullet.BLANK_MARKED) == 0
            ):
                for i in range(len(self.bullets)):
                    if self.bullets[i] is Bullet.UNKNOWN:
                        self.bullets[i] = Bullet.LIVE
            elif (
                self.bullets.count(Bullet.BLANK_MARKED) == 0
                and self.bullets.count(Bullet.LIVE_MARKED) != 0
                and self.live - self.bullets.count(Bullet.LIVE_MARKED) == 0
            ):
                for i in range(len(self.bullets)):
                    if self.bullets[i] is Bullet.UNKNOWN:
                        self.bullets[i] = Bullet.BLANK
