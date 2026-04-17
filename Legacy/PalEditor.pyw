import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path


PALETTE_COLORS = 256
PALETTE_BYTES = 768
GRID_COLS = 16
GRID_ROWS = 16
CELL_SIZE = 24
PREVIEW_SIZE = 96
MAX_VGA = 63


class PalEditorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PAL Editor - VGA 0..63")

        self.current_file: Path | None = None
        self.selected_index = 0
        self.palette = [(0, 0, 0) for _ in range(PALETTE_COLORS)]
        self.cell_ids = []

        self._build_ui()
        self.new_palette()

    def _build_ui(self):
        main = tk.Frame(self.root, padx=10, pady=10)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main)
        left.pack(side="left", fill="both", expand=False)

        right = tk.Frame(main, padx=12)
        right.pack(side="left", fill="y", expand=False)

        topbar = tk.Frame(left)
        topbar.pack(fill="x", pady=(0, 8))

        tk.Button(topbar, text="New", width=10, command=self.new_palette).pack(side="left", padx=2)
        tk.Button(topbar, text="Open", width=10, command=self.open_palette).pack(side="left", padx=2)
        tk.Button(topbar, text="Save", width=10, command=self.save_palette).pack(side="left", padx=2)
        tk.Button(topbar, text="Save As", width=10, command=self.save_palette_as).pack(side="left", padx=2)

        self.file_label = tk.Label(topbar, text="No file", anchor="w")
        self.file_label.pack(side="left", padx=(12, 0))

        canvas_w = GRID_COLS * CELL_SIZE
        canvas_h = GRID_ROWS * CELL_SIZE
        self.canvas = tk.Canvas(left, width=canvas_w, height=canvas_h, highlightthickness=1, highlightbackground="#666")
        self.canvas.pack()

        for row in range(GRID_ROWS):
            row_ids = []
            for col in range(GRID_COLS):
                x0 = col * CELL_SIZE
                y0 = row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                rect_id = self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill="#000000",
                    outline="#444444",
                    width=1
                )
                row_ids.append(rect_id)
            self.cell_ids.append(row_ids)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        tk.Label(right, text="Selected Color", font=("Arial", 11, "bold")).pack(anchor="w")

        self.preview = tk.Canvas(
            right,
            width=PREVIEW_SIZE,
            height=PREVIEW_SIZE,
            highlightthickness=1,
            highlightbackground="#666"
        )
        self.preview.pack(pady=(6, 10))
        self.preview_rect = self.preview.create_rectangle(
            0, 0, PREVIEW_SIZE, PREVIEW_SIZE,
            fill="#000000",
            outline=""
        )

        self.index_var = tk.StringVar(value="Index: 0")
        tk.Label(right, textvariable=self.index_var, font=("Arial", 10)).pack(anchor="w", pady=(0, 10))

        self.r_var = tk.IntVar(value=0)
        self.g_var = tk.IntVar(value=0)
        self.b_var = tk.IntVar(value=0)

        self._make_channel_editor(right, "R", self.r_var)
        self._make_channel_editor(right, "G", self.g_var)
        self._make_channel_editor(right, "B", self.b_var)

        button_row = tk.Frame(right)
        button_row.pack(fill="x", pady=(10, 0))

        tk.Button(button_row, text="Apply RGB", command=self.apply_rgb).pack(side="left", padx=2)
        tk.Button(button_row, text="Set Black", command=self.set_black).pack(side="left", padx=2)
        tk.Button(button_row, text="Set White", command=self.set_white).pack(side="left", padx=2)

        help_text = (
            "Format:\n"
            "- 256 colors\n"
            "- 768 bytes\n"
            "- RGB order\n"
            "- Each channel: 0..63"
        )
        tk.Label(right, text=help_text, justify="left", fg="#444").pack(anchor="w", pady=(16, 0))

    def _make_channel_editor(self, parent, label_text: str, var: tk.IntVar):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=4)

        tk.Label(row, text=label_text, width=2).pack(side="left")

        scale = tk.Scale(
            row,
            from_=0,
            to=MAX_VGA,
            orient="horizontal",
            variable=var,
            showvalue=True,
            length=180,
            command=lambda _=None: self.update_preview_from_vars()
        )
        scale.pack(side="left")

        entry = tk.Entry(row, textvariable=var, width=4, justify="center")
        entry.pack(side="left", padx=(6, 0))
        entry.bind("<KeyRelease>", lambda e: self.update_preview_from_vars())
        entry.bind("<FocusOut>", lambda e: self.clamp_vars())

    def rgb63_to_hex(self, rgb):
        r, g, b = rgb
        r8 = int(r * 255 / 63)
        g8 = int(g * 255 / 63)
        b8 = int(b * 255 / 63)
        return f"#{r8:02x}{g8:02x}{b8:02x}"

    def clamp_vars(self):
        self.r_var.set(max(0, min(MAX_VGA, self.safe_int(self.r_var.get()))))
        self.g_var.set(max(0, min(MAX_VGA, self.safe_int(self.g_var.get()))))
        self.b_var.set(max(0, min(MAX_VGA, self.safe_int(self.b_var.get()))))
        self.update_preview_from_vars()

    def safe_int(self, value):
        try:
            return int(value)
        except Exception:
            return 0

    def new_palette(self):
        self.current_file = None
        self.file_label.config(text="No file")
        self.palette = [(0, 0, 0) for _ in range(PALETTE_COLORS)]
        self.selected_index = 0
        self.refresh_palette_grid()
        self.load_selected_to_controls()

    def open_palette(self):
        path = filedialog.askopenfilename(
            title="Open PAL",
            filetypes=[("PAL files", "*.PAL *.pal"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            data = Path(path).read_bytes()
        except Exception as e:
            messagebox.showerror("Open Error", str(e))
            return

        if len(data) != PALETTE_BYTES:
            messagebox.showerror("Invalid PAL", f"PAL file must be exactly 768 bytes.\nCurrent size: {len(data)}")
            return

        new_palette = []
        for i in range(0, PALETTE_BYTES, 3):
            r = data[i]
            g = data[i + 1]
            b = data[i + 2]
            if r > MAX_VGA or g > MAX_VGA or b > MAX_VGA:
                messagebox.showerror(
                    "Invalid PAL",
                    "This editor expects VGA PAL data in 0..63 range.\n"
                    f"Found value above 63 at byte offset {i}."
                )
                return
            new_palette.append((r, g, b))

        self.palette = new_palette
        self.current_file = Path(path)
        self.file_label.config(text=str(self.current_file))
        self.selected_index = 0
        self.refresh_palette_grid()
        self.load_selected_to_controls()

    def save_palette(self):
        if self.current_file is None:
            self.save_palette_as()
            return
        self._write_palette(self.current_file)

    def save_palette_as(self):
        path = filedialog.asksaveasfilename(
            title="Save PAL As",
            defaultextension=".PAL",
            filetypes=[("PAL files", "*.PAL"), ("All files", "*.*")]
        )
        if not path:
            return
        self.current_file = Path(path)
        self.file_label.config(text=str(self.current_file))
        self._write_palette(self.current_file)

    def _write_palette(self, path: Path):
        try:
            raw = bytearray()
            for r, g, b in self.palette:
                raw.extend((r, g, b))
            path.write_bytes(bytes(raw))
            messagebox.showinfo("Saved", f"Saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def on_canvas_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if not (0 <= col < GRID_COLS and 0 <= row < GRID_ROWS):
            return
        self.selected_index = row * GRID_COLS + col
        self.refresh_palette_grid()
        self.load_selected_to_controls()

    def load_selected_to_controls(self):
        r, g, b = self.palette[self.selected_index]
        self.r_var.set(r)
        self.g_var.set(g)
        self.b_var.set(b)
        self.index_var.set(f"Index: {self.selected_index}")
        self.update_preview_from_vars()

    def update_preview_from_vars(self):
        self.clamp_display_only()
        rgb = (self.safe_int(self.r_var.get()), self.safe_int(self.g_var.get()), self.safe_int(self.b_var.get()))
        self.preview.itemconfig(self.preview_rect, fill=self.rgb63_to_hex(rgb))

    def clamp_display_only(self):
        r = max(0, min(MAX_VGA, self.safe_int(self.r_var.get())))
        g = max(0, min(MAX_VGA, self.safe_int(self.g_var.get())))
        b = max(0, min(MAX_VGA, self.safe_int(self.b_var.get())))
        if r != self.safe_int(self.r_var.get()):
            self.r_var.set(r)
        if g != self.safe_int(self.g_var.get()):
            self.g_var.set(g)
        if b != self.safe_int(self.b_var.get()):
            self.b_var.set(b)

    def apply_rgb(self):
        self.clamp_vars()
        rgb = (
            self.safe_int(self.r_var.get()),
            self.safe_int(self.g_var.get()),
            self.safe_int(self.b_var.get())
        )
        self.palette[self.selected_index] = rgb
        self.refresh_palette_grid()

    def set_black(self):
        self.r_var.set(0)
        self.g_var.set(0)
        self.b_var.set(0)
        self.apply_rgb()

    def set_white(self):
        self.r_var.set(63)
        self.g_var.set(63)
        self.b_var.set(63)
        self.apply_rgb()

    def refresh_palette_grid(self):
        for idx, (r, g, b) in enumerate(self.palette):
            row = idx // GRID_COLS
            col = idx % GRID_COLS
            rect_id = self.cell_ids[row][col]

            outline = "#ffffff" if idx == self.selected_index else "#444444"
            width = 3 if idx == self.selected_index else 1

            self.canvas.itemconfig(
                rect_id,
                fill=self.rgb63_to_hex((r, g, b)),
                outline=outline,
                width=width
            )


def main():
    root = tk.Tk()
    app = PalEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()