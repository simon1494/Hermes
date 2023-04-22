import tkinter as tk
import template
import model

if __name__ == "__main__":
    root = tk.Tk()
    model.create_db()
    template.App(root)
    root.mainloop()
