"""
Automated Screenshot Generator for Space Explorer Application.
Captures GUI window screenshots for the project report document.
"""

import tkinter as tk
from PIL import ImageGrab
import time
import os

from gui_app import SpaceExplorerApp

def capture_widget(widget, filename):
    widget.update()
    widget.update_idletasks()
    
    # Get exact bounding box of the window
    x = widget.winfo_rootx()
    y = widget.winfo_rooty()
    w = widget.winfo_width()
    h = widget.winfo_height()
    
    bbox = (x, y, x + w, y + h)
    
    # Grab image
    img = ImageGrab.grab(bbox=bbox)
    img.save(filename)
    print(f"Saved screenshot: {filename}")

def main():
    root = tk.Tk()
    app = SpaceExplorerApp(root)
    root.geometry("1100x820")
    root.update_idletasks()
    root.update()
    time.sleep(0.5)

    # 1. Output Screenshot (Valid input)
    app.ent_name.delete(0, tk.END)
    app.ent_name.insert(0, "Commander Sarah")
    app.ent_weight.delete(0, tk.END)
    app.ent_weight.insert(0, "75")
    app.ent_age.delete(0, tk.END)
    app.ent_age.insert(0, "28")
    app.on_calculate()
    root.update()
    time.sleep(0.5)
    
    capture_widget(root, "sample_output.png")

    # 2. Validation Error Screenshot
    app.ent_weight.delete(0, tk.END)
    app.ent_weight.insert(0, "-15.5")
    app.on_calculate()
    root.update()
    time.sleep(0.5)

    capture_widget(root, "sample_input_error.png")

    # 3. Chart Window Screenshot
    app.ent_weight.delete(0, tk.END)
    app.ent_weight.insert(0, "75")
    app.on_calculate()
    app.on_show_chart()
    root.update()
    time.sleep(0.5)
    
    if app.chart_window:
        capture_widget(app.chart_window, "sample_chart.png")

    root.destroy()

if __name__ == "__main__":
    main()
