"""Simple Tkinter GUI for Kingdom's Peril.

This is a lightweight, event-driven front-end that displays questions and
options from the text adventure and allows the player to click buttons
instead of typing at the console.

Run with:
    python .\adventure_gui.py

This GUI is intentionally simple and mirrors a subset of the console
game's scenes (main menu, castle/forest choices and a few branches).
It appends outcomes to adventure_outcomes.txt (same file used by the
console game).
"""

import os
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext


OUTCOMES_FILE = os.path.join(os.path.dirname(__file__), "adventure_outcomes.txt")


def save_outcome(outcome: str):
    try:
        with open(OUTCOMES_FILE, "a", encoding="utf-8") as f:
            f.write(outcome + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save outcome: {e}")


def read_outcomes():
    try:
        if not os.path.exists(OUTCOMES_FILE):
            return "No outcomes recorded yet."
        with open(OUTCOMES_FILE, "r", encoding="utf-8") as f:
            contents = f.read().strip()
            return contents if contents else "No outcomes recorded yet."
    except Exception as e:
        return f"Error reading outcomes: {e}"


class AdventureGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kingdom's Peril — GUI")
        self.geometry("640x360")
        self.player_name = "Sir indecisive"

        # Main containers
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.story_label = tk.Label(self.text_frame, text="", wraplength=600, justify=tk.LEFT)
        self.story_label.pack(anchor=tk.w)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Start the flow by asking for name
        self.ask_name()

    def clear_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

    def set_story(self, text: str):
        self.story_label.config(text=text)

    def ask_name(self):
        name = simpledialog.askstring("Knightly Name", "Enter your knightly name:", parent=self)
        if name and name.strip():
            self.player_name = name.strip()
        self.show_main_menu()

    def show_main_menu(self):
        self.set_story(f"Welcome, {self.player_name}!\n\nChoose an option:")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="Start New Adventure", command=self.start_adventure).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="View Past Outcomes", command=self.show_outcomes).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Quit", command=self.quit).pack(side=tk.LEFT, padx=5)

    def show_outcomes(self):
        contents = read_outcomes()
        win = tk.Toplevel(self)
        win.title("Past Outcomes")
        txt = scrolledtext.ScrolledText(win, width=80, height=20)
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, contents)
        txt.config(state=tk.DISABLED)

    # --- Adventure scenes (subset adapted from console version) ---
    def start_adventure(self):
        self.set_story(
            "You are on a quest to rescue Princess Elara. Legend says she's held in the Crimson Castle.\n\nGo to castle or forest?"
        )
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="Castle", command=self.castle_entrance).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Forest", command=self.forest_path).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

    def castle_entrance(self):
        self.set_story("You stand before the massive castle gates. Choose entrance:\n1) Guarded main entrance\n2) Quiet side entrance")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="1", command=self.main_entrance).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="2", command=self.side_entrance).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.start_adventure).pack(side=tk.LEFT, padx=5)

    def main_entrance(self):
        self.set_story("Guards spot you! Choose:\nA) Fight\nB) Diplomacy\nC) Create distraction")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="A", command=lambda: self.fatal("Fell in main entrance combat", "Your bold attack fails and you fall in battle.")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="B", command=lambda: self.save_and_show("Heroically gained entry", "Your silver tongue wins safe passage!", self.grand_hall)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="C", command=lambda: self.save_and_show("Slipped past guards", "Your distraction works and you slip by.", self.grand_hall)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.castle_entrance).pack(side=tk.LEFT, padx=5)

    def side_entrance(self):
        self.set_story("A magical barrier asks: What comes once in a minute, twice in a moment, but never in a thousand years? (Answer single letter)")
        self.clear_buttons()
        entry = tk.Entry(self.buttons_frame)
        entry.pack(side=tk.LEFT, padx=5)

        def attempt():
            ans = entry.get().strip().lower()
            if ans == "m":
                self.save_and_show("Solved side entrance riddle", "The barrier dissolves!", self.secret_library)
            else:
                messagebox.showinfo("Wrong", "That is not the answer. You have failed and the barrier strikes you down.")
                self.fatal("Failed side entrance riddle", "Barrier blast ended your quest.")

        tk.Button(self.buttons_frame, text="Submit", command=attempt).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.castle_entrance).pack(side=tk.LEFT, padx=5)

    def secret_library(self):
        self.set_story("You find an ancient library with two artifacts:\n1) Glowing crystal orb\n2) Dusty tome")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="1", command=lambda: self.save_and_show("Learned secret passages", "The orb reveals secret passages.", self.dungeon_path)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="2", command=lambda: self.fatal("Driven mad by ancient tome", "The tome curses you into madness.")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.castle_entrance).pack(side=tk.LEFT, padx=5)

    def grand_hall(self):
        self.set_story("You enter the grand hall. Left: balcony noises. Right: singing below. Go left or right?")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="Left", command=self.balcony_path).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Right", command=self.dungeons).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.castle_entrance).pack(side=tk.LEFT, padx=5)

    def balcony_path(self):
        self.set_story("Princess Elara is chained on the balcony and the Dark Vizier appears. Fight or Rescue?")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="Fight", command=lambda: self.fatal("Defeated by Dark Vizier", "The Vizier's magic engulfs you.")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Rescue", command=lambda: self.save_and_show("Heroically rescued princess", "You free the princess and escape!", self.show_main_menu)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.grand_hall).pack(side=tk.LEFT, padx=5)

    def dungeons(self):
        self.set_story("Dark stairs lead to dungeons. Choose:\n1) Clanging left\n2) Moaning ahead\n3) Flickering light right")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="1", command=lambda: self.save_and_show("Armed at armory", "You find an armory and better equipment.", self.throne_room)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="2", command=lambda: self.fatal("Fell to dungeon zombies", "Zombies overwhelm you.")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="3", command=lambda: self.save_and_show("Found secret passage", "A torch reveals a passage upward.", self.throne_room)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.grand_hall).pack(side=tk.LEFT, padx=5)

    def throne_room(self):
        self.set_story("You burst into the throne room. The False King taunts you. Charge or Trick?")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="Charge", command=lambda: self.fatal("Fell in throne room", "Magic defenses consume you.")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Trick", command=lambda: self.save_and_show("Saw through throne room illusion", "Your trick exposes the illusion!", self.show_main_menu)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.dungeons).pack(side=tk.LEFT, padx=5)

    def dungeon_path(self):
        self.set_story("You find cells: A) Princess Elara in a cell B) Empty cell with open door")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="A", command=lambda: self.fatal("Fell to dungeon mimic", "The cell was a monster!")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="B", command=lambda: self.save_and_show("Found true princess through intuition", "You find an escape tunnel to the princess.", self.show_main_menu)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.secret_library).pack(side=tk.LEFT, padx=5)

    def forest_path(self):
        self.set_story("You take the forest path. A mystical stag blocks your way. Choose:\n1) Calm it\n2) Shoot it\n3) Follow it\n4) Approach a shining pond nearby")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="1", command=lambda: self.save_and_show("Led to secret entrance", "The stag leads you to a secret castle entrance.", self.secret_library)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="2", command=lambda: self.fatal("Swarmed by forest spirits", "Forest spirits overwhelm you.")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="3", command=lambda: self.druid_quest()).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="4", command=self.mystic_pond).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.start_adventure).pack(side=tk.LEFT, padx=5)

    def druid_quest(self):
        self.set_story("Druids ask: What occurs once in June, twice in August, but never in October? (single letter)")
        self.clear_buttons()
        entry = tk.Entry(self.buttons_frame)
        entry.pack(side=tk.LEFT, padx=5)

        def attempt():
            ans = entry.get().strip().lower()
            if ans == "e":
                self.save_and_show("Druids' amulet granted", "The druids bestow an amulet of protection.", self.throne_room)
            else:
                self.fatal("Failed druid riddle", "The druids' curse ends your quest.")

        tk.Button(self.buttons_frame, text="Submit", command=attempt).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.forest_path).pack(side=tk.LEFT, padx=5)

    def mystic_pond(self):
        self.set_story("You approach a serene pond. A) Drink B) Search banks C) Vow")
        self.clear_buttons()
        tk.Button(self.buttons_frame, text="A", command=lambda: self.save_and_show("Healed by mystic pond and found hidden tunnel", "The water heals you and reveals a hidden tunnel.", self.throne_room)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="B", command=lambda: self.save_and_show("Found medallion at mystic pond", "You find a medallion that repels lesser magic.", self.secret_library)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="C", command=lambda: self.save_and_show("Boon of the pond guardian", "A guardian spirit grants you a boon.", self.throne_room)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.forest_path).pack(side=tk.LEFT, padx=5)

    # --- Helpers ---
    def fatal(self, outcome_short: str, message: str):
        save_outcome(outcome_short)
        messagebox.showinfo("Fatal", message)
        self.show_main_menu()

    def save_and_show(self, outcome_short: str, message: str, next_scene=None):
        save_outcome(outcome_short)
        messagebox.showinfo("Outcome", message)
        if callable(next_scene):
            next_scene()
        else:
            self.show_main_menu()


if __name__ == "__main__":
    app = AdventureGUI()
    app.mainloop()
