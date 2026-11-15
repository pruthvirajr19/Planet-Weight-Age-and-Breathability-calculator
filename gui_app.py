"""
GUI Module for Space Explorer's Guide to the Solar System.
Built with Tkinter, ttk, and Matplotlib.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from calculator_logic import (
    validate_inputs,
    calculate_all_planets,
    get_survival_summary
)
from planet_data import PLANET_DATA

# Deep Space Theme Color Palette
COLOR_BG_DARK = "#0b0f19"         # Outer space background
COLOR_PANEL_BG = "#161e2e"        # Secondary container slate
COLOR_INPUT_BG = "#1e293b"        # Input background
COLOR_TEXT_LIGHT = "#f8fafc"      # Primary text color
COLOR_TEXT_MUTED = "#94a3b8"      # Subtitle/Muted text
COLOR_ACCENT_CYAN = "#00f0ff"     # Primary accent cyan
COLOR_ACCENT_GOLD = "#fbbf24"     # Secondary accent gold
COLOR_SUCCESS_GREEN = "#22c55e"   # Green for breathable
COLOR_DANGER_RED = "#ef4444"      # Red for non-breathable / errors
COLOR_ROW_ALT = "#111827"         # Treeview alternate row
COLOR_ROW_BREATHABLE = "#064e3b"   # Treeview Earth/breathable highlight background

class SpaceExplorerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Space Explorer's Guide to the Solar System")
        self.root.geometry("1100x820")
        self.root.minsize(980, 750)
        self.root.configure(bg=COLOR_BG_DARK)

        # Application state
        self.current_results = []
        self.chart_window = None

        # Configure custom TTK styles
        self._configure_styles()

        # Build UI layout
        self._create_header_frame()
        self._create_input_frame()
        self._create_error_banner()
        self._create_results_table_frame()
        self._create_summary_frame()

        # Bind Enter key to calculation
        self.root.bind("<Return>", lambda event: self.on_calculate())

        # Pre-fill with default example calculation
        self.on_calculate()

    def _configure_styles(self):
        """Sets up custom dark-themed ttk styles for Treeview, Buttons, and Frames."""
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview styling
        style.configure(
            "Treeview",
            background=COLOR_PANEL_BG,
            foreground=COLOR_TEXT_LIGHT,
            fieldbackground=COLOR_PANEL_BG,
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_INPUT_BG,
            foreground=COLOR_ACCENT_CYAN,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=6
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#334155")]
        )
        style.map(
            "Treeview",
            background=[("selected", "#0284c7")],
            foreground=[("selected", "#ffffff")]
        )

    def _create_header_frame(self):
        """Builds top title banner frame."""
        header_frame = tk.Frame(self.root, bg=COLOR_BG_DARK)
        header_frame.pack(fill="x", padx=20, pady=(15, 5))

        title_label = tk.Label(
            header_frame,
            text="🚀 SPACE EXPLORER'S GUIDE TO THE SOLAR SYSTEM 🪐",
            font=("Segoe UI", 20, "bold"),
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_DARK
        )
        title_label.pack(anchor="center")

        subtitle_label = tk.Label(
            header_frame,
            text="Calculate your planetary weight, orbital age, and atmospheric breathability across the 8 planets",
            font=("Segoe UI", 11, "italic"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG_DARK
        )
        subtitle_label.pack(anchor="center", pady=(4, 0))

    def _create_input_frame(self):
        """Builds input panel for Explorer Name, Weight, and Age."""
        input_container = tk.Frame(
            self.root,
            bg=COLOR_PANEL_BG,
            highlightbackground="#334155",
            highlightthickness=1,
            bd=0
        )
        input_container.pack(fill="x", padx=20, pady=10)

        # Section Header
        sec_title = tk.Label(
            input_container,
            text="👨‍🚀 EXPLORER CREDENTIALS & METRICS",
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_ACCENT_GOLD,
            bg=COLOR_PANEL_BG
        )
        sec_title.pack(anchor="w", padx=15, pady=(12, 8))

        fields_frame = tk.Frame(input_container, bg=COLOR_PANEL_BG)
        fields_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Field 1: Name
        lbl_name = tk.Label(
            fields_frame, text="Explorer Name:", font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT_LIGHT, bg=COLOR_PANEL_BG
        )
        lbl_name.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)

        self.ent_name = tk.Entry(
            fields_frame, font=("Segoe UI", 10), bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_TEXT_LIGHT,
            relief="flat", highlightbackground="#475569", highlightthickness=1, width=16
        )
        self.ent_name.grid(row=0, column=1, padx=(0, 20), pady=5)
        self.ent_name.insert(0, "Explorer")

        # Field 2: Weight
        lbl_weight = tk.Label(
            fields_frame, text="Earth Weight (kg):", font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT_LIGHT, bg=COLOR_PANEL_BG
        )
        lbl_weight.grid(row=0, column=2, sticky="w", padx=(0, 5), pady=5)

        self.ent_weight = tk.Entry(
            fields_frame, font=("Segoe UI", 10), bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_TEXT_LIGHT,
            relief="flat", highlightbackground="#475569", highlightthickness=1, width=12
        )
        self.ent_weight.grid(row=0, column=3, padx=(0, 20), pady=5)
        self.ent_weight.insert(0, "70")

        # Field 3: Age
        lbl_age = tk.Label(
            fields_frame, text="Earth Age (years):", font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT_LIGHT, bg=COLOR_PANEL_BG
        )
        lbl_age.grid(row=0, column=4, sticky="w", padx=(0, 5), pady=5)

        self.ent_age = tk.Entry(
            fields_frame, font=("Segoe UI", 10), bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_TEXT_LIGHT,
            relief="flat", highlightbackground="#475569", highlightthickness=1, width=12
        )
        self.ent_age.grid(row=0, column=5, padx=(0, 20), pady=5)
        self.ent_age.insert(0, "25")

        # Buttons Frame
        btn_frame = tk.Frame(fields_frame, bg=COLOR_PANEL_BG)
        btn_frame.grid(row=0, column=6, sticky="e", padx=(10, 0))

        btn_calc = tk.Button(
            btn_frame, text="⚡ Calculate", font=("Segoe UI", 10, "bold"),
            bg="#0284c7", fg="#ffffff", activebackground="#0369a1", activeforeground="#ffffff",
            relief="flat", padx=12, pady=4, cursor="hand2", command=self.on_calculate
        )
        btn_calc.pack(side="left", padx=4)

        btn_reset = tk.Button(
            btn_frame, text="🔄 Reset", font=("Segoe UI", 10, "bold"),
            bg="#334155", fg=COLOR_TEXT_LIGHT, activebackground="#475569", activeforeground="#ffffff",
            relief="flat", padx=10, pady=4, cursor="hand2", command=self.on_reset
        )
        btn_reset.pack(side="left", padx=4)

        btn_chart = tk.Button(
            btn_frame, text="📊 Bar Chart", font=("Segoe UI", 10, "bold"),
            bg="#d97706", fg="#ffffff", activebackground="#b45309", activeforeground="#ffffff",
            relief="flat", padx=10, pady=4, cursor="hand2", command=self.on_show_chart
        )
        btn_chart.pack(side="left", padx=4)

    def _create_error_banner(self):
        """Inline container for validation error messages."""
        self.error_frame = tk.Frame(self.root, bg="#451a1a", highlightbackground=COLOR_DANGER_RED, highlightthickness=1)
        # Initially hidden
        self.lbl_error = tk.Label(
            self.error_frame, text="", font=("Segoe UI", 10, "bold"),
            fg="#fca5a5", bg="#451a1a", padx=10, pady=6
        )
        self.lbl_error.pack(fill="x")

    def _show_error(self, message: str):
        """Displays inline validation error message."""
        self.lbl_error.config(text=f"⚠️ Validation Error: {message}")
        self.error_frame.pack(fill="x", padx=20, pady=(0, 10), before=self.table_container)

    def _hide_error(self):
        """Hides the inline error banner."""
        self.error_frame.pack_forget()

    def _create_results_table_frame(self):
        """Builds styled ttk.Treeview table frame."""
        self.table_container = tk.Frame(
            self.root, bg=COLOR_PANEL_BG,
            highlightbackground="#334155", highlightthickness=1, bd=0
        )
        self.table_container.pack(fill="both", expand=True, padx=20, pady=5)

        # Table title
        table_hdr = tk.Label(
            self.table_container, text="🌍 PLANETARY ENVIRONMENT & METRICS TABLE",
            font=("Segoe UI", 11, "bold"), fg=COLOR_ACCENT_CYAN, bg=COLOR_PANEL_BG
        )
        table_hdr.pack(anchor="w", padx=15, pady=(10, 5))

        # Treeview Columns
        columns = ("planet", "weight", "age", "oxygen", "breathable", "temp", "atmosphere")
        self.tree = ttk.Treeview(self.table_container, columns=columns, show="headings", height=8)

        # Set headings
        self.tree.heading("planet", text="Planet Name")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("age", text="Age (years)")
        self.tree.heading("oxygen", text="Oxygen Level (%)")
        self.tree.heading("breathable", text="Breathable?")
        self.tree.heading("temp", text="Avg Temp (°C)")
        self.tree.heading("atmosphere", text="Main Atmospheric Composition")

        # Set column widths & alignments
        self.tree.column("planet", width=140, anchor="w")
        self.tree.column("weight", width=110, anchor="e")
        self.tree.column("age", width=110, anchor="e")
        self.tree.column("oxygen", width=120, anchor="e")
        self.tree.column("breathable", width=110, anchor="center")
        self.tree.column("temp", width=110, anchor="e")
        self.tree.column("atmosphere", width=260, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 12))
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 12))

        # Tag configurations for row highlighting
        self.tree.tag_configure("breathable_yes", background="#064e3b", foreground="#86efac", font=("Segoe UI", 10, "bold"))
        self.tree.tag_configure("row_even", background="#0f172a", foreground=COLOR_TEXT_LIGHT)
        self.tree.tag_configure("row_odd", background="#1e293b", foreground=COLOR_TEXT_LIGHT)

    def _create_summary_frame(self):
        """Builds bottom survival summary frame."""
        self.summary_container = tk.Frame(
            self.root, bg=COLOR_PANEL_BG,
            highlightbackground="#334155", highlightthickness=1, bd=0
        )
        self.summary_container.pack(fill="x", padx=20, pady=(5, 15))

        sec_title = tk.Label(
            self.summary_container, text="🛰️ SPACE EXPLORER SURVIVAL REPORT",
            font=("Segoe UI", 11, "bold"), fg=COLOR_ACCENT_GOLD, bg=COLOR_PANEL_BG
        )
        sec_title.pack(anchor="w", padx=15, pady=(10, 5))

        # 3 Key Stat Cards Box
        cards_frame = tk.Frame(self.summary_container, bg=COLOR_PANEL_BG)
        cards_frame.pack(fill="x", padx=15, pady=2)

        # Card 1: Heaviest
        self.card_heaviest = tk.Label(
            cards_frame, text="🏋️ Heaviest: --", font=("Segoe UI", 10, "bold"),
            fg="#f8fafc", bg="#1e293b", padx=12, pady=6, relief="flat",
            highlightbackground="#334155", highlightthickness=1
        )
        self.card_heaviest.pack(side="left", expand=True, fill="x", padx=4)

        # Card 2: Lightest
        self.card_lightest = tk.Label(
            cards_frame, text="🪶 Lightest: --", font=("Segoe UI", 10, "bold"),
            fg="#f8fafc", bg="#1e293b", padx=12, pady=6, relief="flat",
            highlightbackground="#334155", highlightthickness=1
        )
        self.card_lightest.pack(side="left", expand=True, fill="x", padx=4)

        # Card 3: Breathable
        self.card_breathable = tk.Label(
            cards_frame, text="🫁 Breathable: --", font=("Segoe UI", 10, "bold"),
            fg="#4ade80", bg="#064e3b", padx=12, pady=6, relief="flat",
            highlightbackground="#22c55e", highlightthickness=1
        )
        self.card_breathable.pack(side="left", expand=True, fill="x", padx=4)

        # Sentence Box
        self.lbl_sentence = tk.Label(
            self.summary_container, text="", font=("Segoe UI", 10),
            fg=COLOR_TEXT_LIGHT, bg="#0f172a", padx=15, pady=8, wraplength=1000, justify="left",
            highlightbackground="#00f0ff", highlightthickness=1
        )
        self.lbl_sentence.pack(fill="x", padx=15, pady=(8, 12))

    def on_calculate(self):
        """Triggered when Calculate button is clicked or Enter is pressed."""
        name_raw = self.ent_name.get()
        weight_raw = self.ent_weight.get()
        age_raw = self.ent_age.get()

        is_valid, name, weight, age, err_msg = validate_inputs(name_raw, weight_raw, age_raw)

        if not is_valid:
            self._show_error(err_msg)
            return

        self._hide_error()

        # Update input entry display cleaned name if defaulted
        if name_raw.strip() == "":
            self.ent_name.delete(0, tk.END)
            self.ent_name.insert(0, "Explorer")

        # Perform calculations
        self.current_results = calculate_all_planets(weight, age)
        summary = get_survival_summary(name, self.current_results)

        # Clear existing Treeview items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Populate table
        for idx, p in enumerate(self.current_results):
            tag = "breathable_yes" if p["is_breathable_bool"] else ("row_even" if idx % 2 == 0 else "row_odd")
            
            planet_disp = f"{p['emoji']} {p['name']}"
            oxygen_disp = f"{p['oxygen_pct']:.2f}%"
            breathable_disp = f"✅ {p['breathable']}" if p["is_breathable_bool"] else f"❌ {p['breathable']}"

            self.tree.insert(
                "", tk.END,
                values=(
                    planet_disp,
                    f"{p['weight']:.2f}",
                    f"{p['age']:.2f}",
                    oxygen_disp,
                    breathable_disp,
                    f"{p['temp_c']} °C",
                    p["main_gas"]
                ),
                tags=(tag,)
            )

        # Update summary panel
        self.card_heaviest.config(text=f"🏋️ Heaviest: {summary['heaviest_planet']} ({summary['heaviest_weight']:.2f} kg)")
        self.card_lightest.config(text=f"🪶 Lightest: {summary['lightest_planet']} ({summary['lightest_weight']:.2f} kg)")
        self.card_breathable.config(text=f"🫁 Breathable Planet: {summary['breathable_planet']} (20.95% O₂)")
        self.lbl_sentence.config(text=summary["summary_sentence"])

        # Update chart window if open
        if self.chart_window is not None and self.chart_window.winfo_exists():
            self._render_chart_in_window()

    def on_reset(self):
        """Resets inputs to defaults and clears table."""
        self._hide_error()
        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, "Explorer")

        self.ent_weight.delete(0, tk.END)
        self.ent_weight.insert(0, "70")

        self.ent_age.delete(0, tk.END)
        self.ent_age.insert(0, "25")

        self.on_calculate()

    def on_show_chart(self):
        """Displays popup Matplotlib bar chart of Weight per Planet."""
        if not self.current_results:
            messagebox.showwarning("No Data", "Please calculate planetary metrics first.")
            return

        if self.chart_window is not None and self.chart_window.winfo_exists():
            self.chart_window.lift()
            return

        self.chart_window = tk.Toplevel(self.root)
        self.chart_window.title("Solar System Planetary Weight & Age Bar Charts")
        self.chart_window.geometry("900x550")
        self.chart_window.configure(bg=COLOR_BG_DARK)

        self._render_chart_in_window()

    def _render_chart_in_window(self):
        """Renders matplotlib subplots inside chart popup window."""
        for widget in self.chart_window.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), facecolor=COLOR_BG_DARK)

        planets = [p["name"] for p in self.current_results]
        weights = [p["weight"] for p in self.current_results]
        ages = [p["age"] for p in self.current_results]

        # Colors for weight bars
        bar_colors_w = []
        for p in self.current_results:
            if p["name"] == "Earth":
                bar_colors_w.append("#22c55e") # Green for Earth
            elif p["name"] == "Jupiter":
                bar_colors_w.append("#f97316") # Orange for Jupiter
            else:
                bar_colors_w.append("#00f0ff") # Cyan

        # Subplot 1: Weight Chart
        bars1 = ax1.bar(planets, weights, color=bar_colors_w, edgecolor="#334155")
        ax1.set_title("Weight across Solar System (kg)", color=COLOR_ACCENT_CYAN, fontsize=12, fontweight="bold")
        ax1.set_ylabel("Weight (kg)", color=COLOR_TEXT_LIGHT)
        ax1.set_facecolor("#161e2e")
        ax1.tick_params(colors=COLOR_TEXT_LIGHT, labelsize=9)
        plt.setp(ax1.get_xticklabels(), rotation=35, ha="right")
        ax1.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.5)

        for bar in bars1:
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{yval:.1f}", ha='center', va='bottom', color=COLOR_TEXT_LIGHT, fontsize=8)

        # Subplot 2: Age Chart
        bar_colors_a = ["#fbbf24" if p["name"]=="Earth" else "#a855f7" for p in self.current_results]
        bars2 = ax2.bar(planets, ages, color=bar_colors_a, edgecolor="#334155")
        ax2.set_title("Orbital Age across Solar System (years)", color=COLOR_ACCENT_GOLD, fontsize=12, fontweight="bold")
        ax2.set_ylabel("Planetary Age (years)", color=COLOR_TEXT_LIGHT)
        ax2.set_facecolor("#161e2e")
        ax2.set_yscale("log") # Log scale because Mercury/Venus age vs Neptune age varies vastly
        ax2.set_ylabel("Age (years, Log Scale)", color=COLOR_TEXT_LIGHT)
        ax2.tick_params(colors=COLOR_TEXT_LIGHT, labelsize=9)
        plt.setp(ax2.get_xticklabels(), rotation=35, ha="right")
        ax2.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.5)

        for bar in bars2:
            yval = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2.0, yval * 1.1, f"{yval:.1f}", ha='center', va='bottom', color=COLOR_TEXT_LIGHT, fontsize=8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
