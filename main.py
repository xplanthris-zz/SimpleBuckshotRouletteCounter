import tkinter as tk
from tkinter import simpledialog, messagebox

class SimpleBuckshotRouletteCounter:
    def __init__(self, master):
        self.master = master
        self.master.title("SimpleBuckshotRouletteCounter")
        self.master.resizable(width=False, height=False)
        self.master.geometry("300x60")
        self.master.attributes("-topmost", True)

        self.live = 0
        self.blank = 0
        self.bullets = []
        self.current_bullet_index = 0

        self.live_label = tk.Label(master, text="Live: 0 (0%)")
        self.live_label.pack()

        self.blank_label = tk.Label(master, text="Blank: 0 (0%)")
        self.blank_label.pack()

        self.live_button = tk.Button(master, text="Live", command=lambda: self.mark_bullet("L"))
        self.live_button.pack(side=tk.LEFT)

        self.new_round_button = tk.Button(master, text="New Round", command=self.new_round)
        self.new_round_button.pack(side=tk.LEFT)

        self.burner_phone_button = tk.Button(master, text="Burner Phone", command=self.use_burner_phone)
        self.burner_phone_button.pack(side=tk.LEFT)

        self.blank_button = tk.Button(master, text="Blank", command=lambda: self.mark_bullet("B"))
        self.blank_button.pack(side=tk.LEFT)

    def new_round(self):
        try:
            total_bullets = simpledialog.askinteger("New Round", "How many bullets are there?", parent=self.master)
            if total_bullets is None:
                return

            if total_bullets > 8:
                messagebox.showerror("Error", "Too many bullets. Maximum allowed is 8.")
                return
            
            if (total_bullets % 2) == 0:
                blank = total_bullets // 2
                live = total_bullets // 2
            else:
                blank = (total_bullets // 2) + 1 
                live = total_bullets // 2

            self.bullets = [None] * total_bullets
            self.live = live
            self.blank = blank
            self.current_bullet_index = 0
            self.update_labels()
        except Exception as e:
            messagebox.showerror("Error", "Invalid input. Please try again.")



    def mark_bullet(self, bullet_type):
        if self.current_bullet_index < len(self.bullets) and self.bullets[self.current_bullet_index] is None:
            self.bullets[self.current_bullet_index] = bullet_type

            if bullet_type == "L":
                if self.live > 0:
                    self.live -= 1
            else:
                if self.blank > 0:
                    self.blank -= 1

            self.autofill_check()
            self.update_labels()

        self.proceed_to_next_bullet()

    def proceed_to_next_bullet(self):        
        self.current_bullet_index += 1
        if self.current_bullet_index < len(self.bullets):
            if self.bullets[self.current_bullet_index] is not None:
                bullet_type = self.bullets[self.current_bullet_index]
                bullet_description = "live" if bullet_type == "L" else "blank"
                messagebox.showinfo("Bullet Predetermined", f"This bullet is a {bullet_description}.")
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

        self.live_label.config(text=f"Live: {self.live} ({live_percent:.2f}%)")
        self.blank_label.config(text=f"Blank: {self.blank} ({blank_percent:.2f}%)")

    def use_burner_phone(self):
        if self.current_bullet_index < len(self.bullets):
            position = simpledialog.askinteger("Burner Phone", "Enter the bullet position (1-indexed):", parent=self.master) - 1
            bullet_type_input = simpledialog.askstring("Burner Phone", "Enter the bullet type (L)ive or (B)lank:", parent=self.master)
        
            if bullet_type_input is not None:
                bullet_type_input = bullet_type_input.strip().upper()
                if bullet_type_input in ["L", "LIVE"]:
                    bullet_type = "L"
                elif bullet_type_input in ["B", "BLANK"]:
                    bullet_type = "B"
                else:
                    messagebox.showerror("Error", "Invalid bullet type. Please enter 'Live' or 'Blank'.")
                    return
            else:
                messagebox.showerror("Error", "No bullet type entered. Please try again.")
                return

            if position is not None and bullet_type in ["L", "B"]:
                self.bullets[position] = bullet_type
                self.autofill_check()
                self.update_labels()
                bullet_description = "live" if bullet_type == "L" else "blank"
                messagebox.showinfo("Burner Phone", f"The bullet at position {position + 1} is marked as {bullet_description}.")
            else:
                messagebox.showerror("Error", "Invalid input. Please try again.")
        else:
            messagebox.showinfo("Round Complete", "This round has ended. Starting a new round.")
            self.new_round()

    def autofill_check(self):
        remaining_slots = self.bullets.count(None)
        if remaining_slots == self.live:
            for i in range(len(self.bullets)):
                if self.bullets[i] is None:
                    self.bullets[i] = "L"
                    if self.live > 0: 
                        self.live -= 1
        elif remaining_slots == self.blank:
            for i in range(len(self.bullets)):
                if self.bullets[i] is None:
                    self.bullets[i] = "B"
                    if self.blank > 0:
                        self.blank -= 1

        self.update_labels()

def main():
    root = tk.Tk()
    app = SimpleBuckshotRouletteCounter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
