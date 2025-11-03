"""Tkinter GUI for Kingdom's Peril using the shared game engine.

Run with:
    python .\adventure_gui.py
"""

import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from game_engine import ENGINE, read_outcomes


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
        self.story_label.pack(anchor=tk.W)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        # Game state
        self.session = None

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

    # --- Engine-driven adventure ---
    def start_adventure(self):
        self.session = ENGINE.new_session(self.player_name)
        self.render_scene()

    def render_scene(self):
        scene = self.session.current_scene()
        self.set_story(self.session.render_text())
        self.clear_buttons()
        if scene.type == "choice":
            for opt in scene.options:
                tk.Button(
                    self.buttons_frame,
                    text=f"{opt.key}: {opt.label}",
                    command=lambda k=opt.key: self.handle_choice(k),
                ).pack(side=tk.LEFT, padx=5)
            tk.Button(self.buttons_frame, text="Inventory", command=self.show_inventory).pack(side=tk.LEFT, padx=5)
            tk.Button(self.buttons_frame, text="Back to Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)
        elif scene.type == "input":
            entry = tk.Entry(self.buttons_frame)
            entry.pack(side=tk.LEFT, padx=5)
            tk.Button(self.buttons_frame, text="Submit", command=lambda: self.handle_input(entry.get())).pack(side=tk.LEFT, padx=5)
            tk.Button(self.buttons_frame, text="Back to Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)
        else:
            # end scenes not used directly; return to menu
            tk.Button(self.buttons_frame, text="Back to Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

    def handle_choice(self, key: str):
        message, is_fatal, is_end = self.session.apply_choice(key)
        if message:
            messagebox.showinfo("Outcome", message)
        if is_end:
            if is_fatal:
                messagebox.showinfo("Quest Ended", "Alas, your quest has ended in tragedy!")
            else:
                messagebox.showinfo("Victory", "Your quest concludes gloriously.")
            self.show_main_menu()
            return
        self.render_scene()

    def handle_input(self, value: str):
        message, is_fatal, is_end = self.session.apply_input(value)
        if message:
            messagebox.showinfo("Outcome", message)
        if is_end:
            if is_fatal:
                messagebox.showinfo("Quest Ended", "Alas, your quest has ended in tragedy!")
            else:
                messagebox.showinfo("Victory", "Your quest concludes gloriously.")
            self.show_main_menu()
            return
        self.render_scene()

    def show_inventory(self):
        if not self.session:
            return
        inv = self.session.describe_inventory()
        messagebox.showinfo("Inventory", f"You carry: {inv}")


if __name__ == "__main__":
    app = AdventureGUI()
    app.mainloop()
