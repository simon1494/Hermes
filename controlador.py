"""
Controlador:
    Administra el flujo de ejecución principal de nuestra aplicación. 
"""


class Controlador:
    def __init__(self, modelo):
        self.modelo = modelo

    def dar_de_alta(self):
        self.modelo.alta_db()

    def da_de_baja(self):
        self.modelo.baja_db()

    def modificar(self):
        self.modelo.modificar_db()

    def consultar(self):
        self.modelo.consultar_db()


if __name__ == "__main__":
    import sys

    sys.path.append("../library")
    import threading
    from tkinter import Tk
    from vista.vista import App
    from vista.logo_inicio import LogoInicio
    from modelos.operaciones_base import DatabaseOps

    def lanzar_inicio():
        logueo = LogoInicio()

    hilo_inicio = threading.Thread(target=lanzar_inicio)
    hilo_inicio.start()
    hilo_inicio.join()

    DatabaseOps.crear_db()

    root = Tk()

    app = App(root)

    app.crear_variables_control()
    app.crear_estilos_y_fuentes()
    app.crear_labels()
    app.crear_entries()
    app.crear_botones()
    app.crear_combo_boxes()
    app.crear_y_armar_treeview()
    app.correr()
