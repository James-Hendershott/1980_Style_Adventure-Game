import tkinter as tk
from tkinter import font as tkfont


class RetroMonitor(tk.Frame):
    """
    A composite widget that draws a retro CRT monitor bezel and embeds an inner
    'screen' frame. Children should be added to self.screen (a tk.Frame).
    """

    def __init__(self, master=None, width=800, height=520, screen_margin=30, screen_radius=18, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#c1b37a")  # vintage beige around the bezel

        self.width = width
        self.height = height
        self.screen_margin = screen_margin
        self.screen_radius = screen_radius

        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0, bd=0, bg="#c1b37a")
        self.canvas.pack()

        # Outer bezel
        self._rounded_rect(
            self.canvas,
            5, 5, width - 5, height - 5,
            r=22,
            fill="#cdbf8b",
            outline="#9e9162",
            width=3,
        )

        # Inner bezel border
        inner_pad = 14
        self._rounded_rect(
            self.canvas,
            inner_pad, inner_pad, width - inner_pad, height - inner_pad,
            r=18,
            fill="#b3a46f",
            outline="#7f734c",
            width=2,
        )

        # Screen area
        sx1 = screen_margin
        sy1 = screen_margin
        sx2 = width - screen_margin
        sy2 = height - screen_margin - 35  # leave a bottom gap like old monitors

        self._rounded_rect(
            self.canvas,
            sx1, sy1, sx2, sy2,
            r=screen_radius,
            fill="#000000",
            outline="#162515",
            width=2,
        )

        # Create the real screen frame inside the canvas 'screen' area
        self.screen = tk.Frame(self.canvas, bg="#000000")
        self.screen_id = self.canvas.create_window(
            (sx1 + sx2) // 2,
            (sy1 + sy2) // 2,
            window=self.screen,
            width=(sx2 - sx1) - 24,
            height=(sy2 - sy1) - 24,
        )

        # Decorative power light and label
        self.canvas.create_oval(width - 70, height - 28, width - 54, height - 12, fill="#2ee55f", outline="#0c7f27")
        self.canvas.create_text(70, height - 22, text="KINGDOM'S PERIL", fill="#3a3a3a", font=("Courier New", 12, "bold"))

        # Add subtle scanlines
        self._draw_scanlines(sx1 + 6, sy1 + 6, sx2 - 6, sy2 - 6, step=4, color="#021a06")

        # Provide a retro font handle
        self.retro_font = tkfont.Font(family="Courier New", size=14)
        self.retro_color = "#00ff66"

    def _rounded_rect(self, canvas, x1, y1, x2, y2, r=10, **kwargs):
        # Approximate rounded rectangle with arcs + rectangles
        canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style=tk.ARC, outline=kwargs.get("outline", ""), width=kwargs.get("width", 1))
        canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style=tk.ARC, outline=kwargs.get("outline", ""), width=kwargs.get("width", 1))
        canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style=tk.ARC, outline=kwargs.get("outline", ""), width=kwargs.get("width", 1))
        canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style=tk.ARC, outline=kwargs.get("outline", ""), width=kwargs.get("width", 1))
        # Filled body
        canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=kwargs.get("fill", ""), outline="")
        canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=kwargs.get("fill", ""), outline="")
        # Outline pass to match fill arcs (simple illusion)
        if kwargs.get("outline"):
            canvas.create_rectangle(x1 + r, y1, x2 - r, y1, outline=kwargs.get("outline"), width=kwargs.get("width", 1))
            canvas.create_rectangle(x1 + r, y2, x2 - r, y2, outline=kwargs.get("outline"), width=kwargs.get("width", 1))

    def _draw_scanlines(self, x1, y1, x2, y2, step=4, color="#021a06"):
        for y in range(int(y1), int(y2), step):
            self.canvas.create_line(x1, y, x2, y, fill=color)
