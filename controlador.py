"""
Controlador:
    Administra la ejecución de nuestra aplicación. 
"""
import sys

sys.path.append("../library")
import tkinter as tk
from vista.vista import App
from vista.logo_inicio import LogoInicio
import threading

if __name__ == "__main__":

    def lanzar_inicio():
        logueo = LogoInicio()

    hilo_inicio = threading.Thread(target=lanzar_inicio)

    hilo_inicio.start()
    hilo_inicio.join()
    root = tk.Tk()
    App(root)
    root.mainloop()
