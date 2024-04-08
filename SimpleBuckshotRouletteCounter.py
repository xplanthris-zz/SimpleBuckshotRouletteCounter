# TODO: Put application logic here
# TODO: Switch to return-oriented OOP
# TODO: Add inverter support
# TODO: Find a replacement for simpledialog / messagebox

from Bullet import Bullet
from tkinter import simpledialog, messagebox
import customtkinter as ctk


class SimpleBuckshotRouletteCounter:
    def __init__(self, master):
        self.master = master
        self.master.title("SimpleBuckshotRouletteCounter")
        self.master.resizable(width=False, height=False)
        self.master.geometry("300x150")
        self.master.attributes("-topmost", True)

        self.live = 0
        self.blank = 0
        self.bullets = []
        self.current_bullet_index = 0

        self.live_label = ctk.CTkLabel(master, text="Live: 0 (0%)")
        self.live_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=10)

        self.blank_label = ctk.CTkLabel(master, text="Blank: 0 (0%)")
        self.blank_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        self.live_button = ctk.CTkButton(master, text="Live", command=lambda: self.mark_bullet(Bullet.LIVE), fg_color="red")
        self.live_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.blank_button = ctk.CTkButton(master, text="Blank", command=lambda: self.mark_bullet(Bullet.BLANK), fg_color="blue")
        self.blank_button.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.new_round_button = ctk.CTkButton(master, text="New Round", command=self.new_round, fg_color="grey")
        self.new_round_button.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.burner_phone_button = ctk.CTkButton(master, text="Burner Phone", command=self.use_burner_phone, fg_color="grey")
        self.burner_phone_button.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def new_round(self):
        try:
            total_bullets = simpledialog.askinteger("New Round", "How many bullets are there?", parent=self.master, minvalue=2, maxvalue=8)
            if total_bullets is None:
                return

            live = total_bullets // 2
            blank = total_bullets - live

            self.bullets = [Bullet.UNKNOWN] * total_bullets
            self.live = live
            self.blank = blank
            self.current_bullet_index = 0

            self.update_labels()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input or error occurred: {e}. Please try again.")

    def mark_bullet(self, bullet_type):
        if self.current_bullet_index < len(self.bullets) and self.bullets[self.current_bullet_index] is Bullet.UNKNOWN:
            self.bullets[self.current_bullet_index] = bullet_type
            if bullet_type == Bullet.LIVE and self.live > 0:
                self.live -= 1
            elif bullet_type == Bullet.BLANK and self.blank > 0:
                self.blank -= 1

            self.autofill_check()
            self.update_labels()

        self.proceed_to_next_bullet()

    def proceed_to_next_bullet(self):
        self.current_bullet_index += 1
        if self.current_bullet_index < len(self.bullets):
            if self.bullets[self.current_bullet_index] is not Bullet.UNKNOWN:
                bullet_type = self.bullets[self.current_bullet_index]
                bullet_description = "live" if bullet_type in [Bullet.LIVE, Bullet.LIVE_MARKED] else "blank"
                messagebox.showinfo("Bullet Predetermined", f"This bullet is a {bullet_description}.")
                if bullet_description == "live":
                    self.live -= 1
                    # Turn marked bullets into unmarked as we have seen them
                    self.bullets[self.current_bullet_index] = Bullet.LIVE
                else:
                    self.blank -= 1
                    # Turn marked bullets into unmarked as we have seen them
                    self.bullets[self.current_bullet_index] = Bullet.BLANK
                self.update_labels()
                self.proceed_to_next_bullet()
        else:
            messagebox.showinfo("Round Complete", "This round has ended. Starting a new round.")
            self.new_round()

    def update_labels(self):
        total_bullets = self.live + self.blank
        if total_bullets > 0:
            live_percent = self.live / total_bullets * 100
            blank_percent = self.blank / total_bullets * 100
        else:
            live_percent = 0
            blank_percent = 0

        self.live_label.configure(text=f"Live: {self.live} ({live_percent:.2f}%)")
        self.blank_label.configure(text=f"Blank: {self.blank} ({blank_percent:.2f}%)")

    def use_burner_phone(self):
        if self.current_bullet_index < len(self.bullets):
            position = simpledialog.askinteger("Burner Phone", "Enter the bullet position (1-indexed):", parent=self.master) - 1
            if position is None or position < 0 or position >= len(self.bullets):
                messagebox.showerror("Error", "Invalid bullet position.")
                return

            bullet_type_input = simpledialog.askstring("Burner Phone", "Enter the bullet type (L)ive or (B)lank:", parent=self.master)
            if bullet_type_input is None:
                messagebox.showerror("Error", "No bullet type entered. Please try again.")
                return

            bullet_type_input = bullet_type_input.strip().upper()
            if bullet_type_input not in ["L", "B", "LIVE", "BLANK"]:
                messagebox.showerror("Error", "Invalid bullet type. Please enter 'Live' or 'Blank'.")
                return
            
            # We mark burner phone bullets in a special way so that autofill does not s*** itself
            if bullet_type_input in ["L", "LIVE"]:
                bullet_type_input = Bullet.LIVE_MARKED
            else:
                bullet_type_input = Bullet.BLANK_MARKED

            self.bullets[position] = bullet_type_input
            self.autofill_check()
            self.update_labels()
            bullet_description = "live" if bullet_type_input == "LM" else "blank"
            messagebox.showinfo("Burner Phone", f"The bullet at position {position + 1} is marked as {bullet_description}.")
        else:
            messagebox.showinfo("Round Complete", "This round has ended. Starting a new round.")
            self.new_round()

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
            if self.bullets.count(Bullet.BLANK_MARKED) != 0 and self.bullets.count(Bullet.LIVE_MARKED) == 0 and self.blank - self.bullets.count(Bullet.BLANK_MARKED) == 0:
                for i in range(len(self.bullets)):
                    if self.bullets[i] is Bullet.UNKNOWN:
                        self.bullets[i] = Bullet.LIVE
            elif self.bullets.count(Bullet.BLANK_MARKED) == 0 and self.bullets.count(Bullet.LIVE_MARKED) != 0 and self.live - self.bullets.count(Bullet.LIVE_MARKED) == 0:
                for i in range(len(self.bullets)):
                    if self.bullets[i] is Bullet.UNKNOWN:
                        self.bullets[i] = Bullet.BLANK