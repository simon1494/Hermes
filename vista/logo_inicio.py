import sys

sys.path.append("../library")
import tkinter as tk
from PIL import Image, ImageTk
from vista.modelos_vista import MetodosBaseVentanas


class LogoInicio(MetodosBaseVentanas):
    def __init__(
        self,
        display_time=5000,
    ):
        self.image_path = "hermes_inicio.jpg"
        self.width = 573
        self.height = 275
        self.display_time = display_time
        self.root = tk.Tk()
        self.root.title("")
        self.root.protocol("WM_DELETE_WINDOW", self.hacer_nada)
        self.root.geometry(self.centrar_ventana(self.width, self.height))
        self.show_image()

    def show_image(self):
        # Carga la imagen usando PIL
        image = Image.open(self.image_path)
        image = image.resize((self.width, self.height))
        photo = ImageTk.PhotoImage(image)

        # Crea un widget Label y configúralo para mostrar la imagen
        label = tk.Label(self.root, image=photo)
        label.pack()
        self.root.after(6000, self.root.destroy)
        self.root.mainloop()

    def hacer_nada(self):
        ...
