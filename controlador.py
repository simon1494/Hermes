"""
Controlador:
    Administra la ejecución de nuestra aplicación. 
"""
import tkinter as tk
from vista import App

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
