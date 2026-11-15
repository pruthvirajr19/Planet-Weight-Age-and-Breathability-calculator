"""
Render High-Resolution Project Screenshots using PIL and Matplotlib.
Generates sample_output.png, sample_input_error.png, and sample_chart.png
for inclusion in the Project Report and documentation.
"""

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
from calculator_logic import calculate_all_planets, get_survival_summary

# Deep Space Theme Colors
COLOR_BG_DARK = "#0b0f19"
COLOR_PANEL_BG = "#161e2e"
COLOR_INPUT_BG = "#1e293b"
COLOR_TEXT_LIGHT = "#f8fafc"
COLOR_TEXT_MUTED = "#94a3b8"
COLOR_ACCENT_CYAN = "#00f0ff"
COLOR_ACCENT_GOLD = "#fbbf24"
COLOR_SUCCESS_GREEN = "#22c55e"
COLOR_DANGER_RED = "#ef4444"

def get_font(size=14, bold=False):
    try:
        font_path = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def create_ui_screenshot(filename, error_msg=None, weight="75", age="28", name="Commander Sarah"):
    width, height = 1100, 820
    img = Image.new("RGB", (width, height), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, bold=True)
    f_sub = get_font(12, bold=False)
    f_sec = get_font(13, bold=True)
    f_label = get_font(11, bold=True)
    f_input = get_font(11, bold=False)
    f_table_hdr = get_font(11, bold=True)
    f_table_cell = get_font(11, bold=False)
    f_table_bold = get_font(11, bold=True)

    # 1. Title Header Banner
    draw.text((width // 2, 22), "SPACE EXPLORER'S GUIDE TO THE SOLAR SYSTEM", fill=COLOR_ACCENT_CYAN, font=f_title, anchor="mt")
    draw.text((width // 2, 56), "Calculate your planetary weight, orbital age, and atmospheric breathability across the 8 planets", fill=COLOR_TEXT_MUTED, font=f_sub, anchor="mt")

    y_offset = 90

    # 2. Input Container
    input_box = [20, y_offset, width - 20, y_offset + 90]
    draw.rectangle(input_box, fill=COLOR_PANEL_BG, outline="#334155", width=1)
    draw.text((35, y_offset + 10), "[+] EXPLORER CREDENTIALS & METRICS", fill=COLOR_ACCENT_GOLD, font=f_sec)

    # Input Fields
    # Name
    draw.text((35, y_offset + 48), "Explorer Name:", fill=COLOR_TEXT_LIGHT, font=f_label)
    draw.rectangle([145, y_offset + 42, 280, y_offset + 72], fill=COLOR_INPUT_BG, outline="#475569")
    draw.text((155, y_offset + 48), name, fill=COLOR_TEXT_LIGHT, font=f_input)

    # Weight
    draw.text((300, y_offset + 48), "Earth Weight (kg):", fill=COLOR_TEXT_LIGHT, font=f_label)
    draw.rectangle([435, y_offset + 42, 525, y_offset + 72], fill=COLOR_INPUT_BG, outline="#475569" if not error_msg else COLOR_DANGER_RED)
    draw.text((445, y_offset + 48), weight, fill=COLOR_TEXT_LIGHT if not error_msg else COLOR_DANGER_RED, font=f_input)

    # Age
    draw.text((545, y_offset + 48), "Earth Age (years):", fill=COLOR_TEXT_LIGHT, font=f_label)
    draw.rectangle([680, y_offset + 42, 760, y_offset + 72], fill=COLOR_INPUT_BG, outline="#475569")
    draw.text((690, y_offset + 48), age, fill=COLOR_TEXT_LIGHT, font=f_input)

    # Buttons
    # Calculate Button
    draw.rectangle([780, y_offset + 42, 875, y_offset + 72], fill="#0284c7")
    draw.text((827, y_offset + 48), "Calculate", fill="#ffffff", font=f_label, anchor="mt")

    # Reset Button
    draw.rectangle([885, y_offset + 42, 955, y_offset + 72], fill="#334155")
    draw.text((920, y_offset + 48), "Reset", fill="#ffffff", font=f_label, anchor="mt")

    # Chart Button
    draw.rectangle([965, y_offset + 42, 1075, y_offset + 72], fill="#d97706")
    draw.text((1020, y_offset + 48), "Bar Chart", fill="#ffffff", font=f_label, anchor="mt")

    y_offset += 100

    # Error Alert Banner (if error_msg exists)
    if error_msg:
        err_box = [20, y_offset, width - 20, y_offset + 38]
        draw.rectangle(err_box, fill="#451a1a", outline=COLOR_DANGER_RED, width=1)
        draw.text((35, y_offset + 9), f"[!] Validation Error: {error_msg}", fill="#fca5a5", font=f_sec)
        y_offset += 48

    # 3. Table Container
    table_top = y_offset
    table_height = 360
    draw.rectangle([20, table_top, width - 20, table_top + table_height], fill=COLOR_PANEL_BG, outline="#334155", width=1)
    draw.text((35, table_top + 10), "[*] PLANETARY ENVIRONMENT & METRICS TABLE", fill=COLOR_ACCENT_CYAN, font=f_sec)

    # Table Header Row
    th_y = table_top + 40
    draw.rectangle([35, th_y, width - 35, th_y + 32], fill=COLOR_INPUT_BG)
    
    cols = [
        ("Planet Name", 45, "left"),
        ("Weight (kg)", 190, "right"),
        ("Age (years)", 300, "right"),
        ("Oxygen Level (%)", 410, "right"),
        ("Breathable?", 540, "center"),
        ("Avg Temp (°C)", 660, "right"),
        ("Main Atmospheric Composition", 780, "left")
    ]
    for title, x_pos, align in cols:
        draw.text((x_pos, th_y + 7), title, fill=COLOR_ACCENT_CYAN, font=f_table_hdr)

    # Calculate metrics (if error, show default baseline in table while error banner is active)
    try:
        w_flt = float(weight)
        a_flt = float(age)
        if w_flt <= 0 or a_flt <= 0:
            raise ValueError()
        results = calculate_all_planets(w_flt, a_flt)
    except Exception:
        results = calculate_all_planets(70.0, 25.0)

    # Table Data Rows
    tr_y = th_y + 32
    for idx, p in enumerate(results):
        row_bg = "#064e3b" if p["is_breathable_bool"] else ("#0f172a" if idx % 2 == 0 else "#1e293b")
        text_fg = "#86efac" if p["is_breathable_bool"] else COLOR_TEXT_LIGHT
        font_use = f_table_bold if p["is_breathable_bool"] else f_table_cell

        draw.rectangle([35, tr_y, width - 35, tr_y + 30], fill=row_bg)

        draw.text((45, tr_y + 6), f"• {p['name']}", fill=text_fg, font=font_use)
        draw.text((250, tr_y + 6), f"{p['weight']:.2f}", fill=text_fg, font=font_use, anchor="ra")
        draw.text((370, tr_y + 6), f"{p['age']:.2f}", fill=text_fg, font=font_use, anchor="ra")
        draw.text((500, tr_y + 6), f"{p['oxygen_pct']:.2f}%", fill=text_fg, font=font_use, anchor="ra")
        
        breath_str = f"Yes (Breathable)" if p["is_breathable_bool"] else f"No"
        draw.text((540, tr_y + 6), breath_str, fill=text_fg, font=font_use)
        draw.text((720, tr_y + 6), f"{p['temp_c']} °C", fill=text_fg, font=font_use, anchor="ra")
        draw.text((780, tr_y + 6), p["main_gas"], fill=text_fg, font=font_use)

        tr_y += 30

    y_offset = table_top + table_height + 15

    # 4. Survival Summary Container
    draw.rectangle([20, y_offset, width - 20, height - 20], fill=COLOR_PANEL_BG, outline="#334155", width=1)
    draw.text((35, y_offset + 10), "[^] SPACE EXPLORER SURVIVAL REPORT", fill=COLOR_ACCENT_GOLD, font=f_sec)

    summary = get_survival_summary(name if not error_msg else "Explorer", results)

    # 3 Stat Cards
    card_y = y_offset + 38
    # Card 1
    draw.rectangle([35, card_y, 360, card_y + 36], fill=COLOR_INPUT_BG, outline="#334155")
    draw.text((45, card_y + 8), f"Heaviest: {summary['heaviest_planet']} ({summary['heaviest_weight']:.2f} kg)", fill=COLOR_TEXT_LIGHT, font=f_label)

    # Card 2
    draw.rectangle([375, card_y, 700, card_y + 36], fill=COLOR_INPUT_BG, outline="#334155")
    draw.text((385, card_y + 8), f"Lightest: {summary['lightest_planet']} ({summary['lightest_weight']:.2f} kg)", fill=COLOR_TEXT_LIGHT, font=f_label)

    # Card 3
    draw.rectangle([715, card_y, 1065, card_y + 36], fill="#064e3b", outline=COLOR_SUCCESS_GREEN)
    draw.text((725, card_y + 8), f"Breathable: {summary['breathable_planet']} (20.95% O2)", fill="#86efac", font=f_label)

    # Sentence Box
    sent_y = card_y + 46
    draw.rectangle([35, sent_y, 1065, sent_y + 40], fill="#0f172a", outline=COLOR_ACCENT_CYAN)
    draw.text((45, sent_y + 10), summary["summary_sentence"], fill=COLOR_TEXT_LIGHT, font=f_sub)

    img.save(filename)
    print(f"Generated UI Screenshot: {filename}")

def render_chart_screenshot(filename, weight=75.0, age=28.0):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 6), facecolor=COLOR_BG_DARK)

    results = calculate_all_planets(weight, age)
    planets = [p["name"] for p in results]
    weights = [p["weight"] for p in results]
    ages = [p["age"] for p in results]

    # Bar colors
    bar_colors_w = ["#22c55e" if p["name"]=="Earth" else ("#f97316" if p["name"]=="Jupiter" else "#00f0ff") for p in results]

    # Subplot 1: Weight Chart
    bars1 = ax1.bar(planets, weights, color=bar_colors_w, edgecolor="#334155")
    ax1.set_title("Planetary Weight Comparison (kg)", color=COLOR_ACCENT_CYAN, fontsize=12, fontweight="bold")
    ax1.set_ylabel("Weight (kg)", color=COLOR_TEXT_LIGHT, fontsize=10)
    ax1.set_facecolor("#161e2e")
    ax1.tick_params(colors=COLOR_TEXT_LIGHT, labelsize=9)
    plt.setp(ax1.get_xticklabels(), rotation=35, ha="right")
    ax1.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.5)

    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}", ha='center', va='bottom', color=COLOR_TEXT_LIGHT, fontsize=8, fontweight="bold")

    # Subplot 2: Age Chart
    bar_colors_a = ["#fbbf24" if p["name"]=="Earth" else "#a855f7" for p in results]
    bars2 = ax2.bar(planets, ages, color=bar_colors_a, edgecolor="#334155")
    ax2.set_title("Orbital Age Comparison (years, Log Scale)", color=COLOR_ACCENT_GOLD, fontsize=12, fontweight="bold")
    ax2.set_ylabel("Planetary Age (years)", color=COLOR_TEXT_LIGHT, fontsize=10)
    ax2.set_facecolor("#161e2e")
    ax2.set_yscale("log")
    ax2.tick_params(colors=COLOR_TEXT_LIGHT, labelsize=9)
    plt.setp(ax2.get_xticklabels(), rotation=35, ha="right")
    ax2.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.5)

    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f"{yval:.1f}", ha='center', va='bottom', color=COLOR_TEXT_LIGHT, fontsize=8, fontweight="bold")

    fig.tight_layout()
    plt.savefig(filename, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated Chart Screenshot: {filename}")

if __name__ == "__main__":
    create_ui_screenshot("sample_output.png", error_msg=None, weight="75", age="28", name="Commander Sarah")
    create_ui_screenshot("sample_input_error.png", error_msg="Weight must be a positive number greater than 0 kg.", weight="-15.5", age="28", name="Explorer")
    render_chart_screenshot("sample_chart.png", weight=75.0, age=28.0)
