"""Tkinter GUI for Kingdom's Peril using the shared game engine.

Run with:
    python .\adventure_gui.py
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import simpledialog, messagebox, scrolledtext
from game_engine import ENGINE, read_outcomes
from retro_monitor import RetroMonitor


class AdventureGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kingdom's Peril — CRT GUI")
        self.geometry("860x600")
        self.player_name = "Sir indecisive"

        # Retro monitor skin
        self.monitor = RetroMonitor(self, width=820, height=520)
        self.monitor.pack(padx=10, pady=10)

        # Screen interior: stack story and buttons
        self.screen_container = tk.Frame(self.monitor.screen, bg="#000000")
        self.screen_container.pack(fill=tk.BOTH, expand=True)
        # Update wrap length on resize so text never clips
        self.screen_container.bind("<Configure>", self._on_resize)

        self.retro_font = tkfont.Font(family="Courier New", size=14)
        self.phosphor = "#00ff66"

        self.story_label = tk.Label(
            self.screen_container,
            text="",
            wraplength=740,
            justify=tk.LEFT,
            bg="#000000",
            fg=self.phosphor,
            font=self.retro_font,
        )
        self.story_label.pack(anchor=tk.W, padx=16, pady=(12, 6))

        self.buttons_frame = tk.Frame(self.screen_container, bg="#000000")
        self.buttons_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
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
        self._crt_button(self.buttons_frame, "Start New Adventure", self.start_adventure).pack(side=tk.LEFT, padx=6)
        self._crt_button(self.buttons_frame, "View Past Outcomes", self.show_outcomes).pack(side=tk.LEFT, padx=6)
        self._crt_button(self.buttons_frame, "Quit", self.quit).pack(side=tk.LEFT, padx=6)

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
                self._crt_button(
                    self.buttons_frame,
                    f"{opt.key}: {opt.label}",
                    lambda k=opt.key: self.handle_choice(k),
                ).pack(fill=tk.X, anchor=tk.W, padx=6, pady=3)
            row = tk.Frame(self.buttons_frame, bg="#000000")
            row.pack(fill=tk.X, padx=0, pady=(6, 0))
            self._crt_button(row, "Inventory", self.show_inventory).pack(side=tk.LEFT, padx=6)
            self._crt_button(row, "Back to Menu", self.show_main_menu).pack(side=tk.LEFT, padx=6)
        elif scene.type == "input":
            entry = tk.Entry(self.buttons_frame, bg="#000000", fg=self.phosphor, insertbackground=self.phosphor, relief=tk.FLAT)
            entry.configure(font=self.retro_font)
            entry.pack(fill=tk.X, padx=6, pady=(0, 6))
            row = tk.Frame(self.buttons_frame, bg="#000000")
            row.pack(fill=tk.X)
            self._crt_button(row, "Submit", lambda: self.handle_input(entry.get())).pack(side=tk.LEFT, padx=6)
            self._crt_button(row, "Back to Menu", self.show_main_menu).pack(side=tk.LEFT, padx=6)
        else:
            # end scenes not used directly; return to menu
            self._crt_button(self.buttons_frame, "Back to Menu", self.show_main_menu).pack(side=tk.LEFT, padx=6)

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

    # --- Styling helpers ---
    def _crt_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#001a00",
            fg=self.phosphor,
            activebackground="#003300",
            activeforeground=self.phosphor,
            relief=tk.FLAT,
            bd=0,
            font=self.retro_font,
            highlightthickness=0,
        )

    def _on_resize(self, event):
        # Keep story text wrapping within available width, leaving some padding
        w = max(event.width - 40, 300)
        self.story_label.configure(wraplength=w)


if __name__ == "__main__":
    app = AdventureGUI()
    app.mainloop()
