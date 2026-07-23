import sys
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()
messagebox.showinfo("Python Version", f"Python version is:\n\n{sys.version}")
