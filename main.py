"""
Main Launcher Script for Space Explorer's Guide to the Solar System.
"""

import tkinter as tk
from gui_app import SpaceExplorerApp

def main():
    root = tk.Tk()
    app = SpaceExplorerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
