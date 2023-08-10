import sys

sys.path.append("../library")

if __name__ == "__main__":
    import threading
    from tkinter import Tk
    from clases.logo_inicio import LogoInicio
    from modelo import Modelo
    from vista import Vista
    from clases.controlador import Controlador
    from clases.estructura_base import DB

    def lanzar_inicio():
        logueo = LogoInicio()

    hilo_inicio = threading.Thread(target=lanzar_inicio)
    hilo_inicio.start()
    hilo_inicio.join()

    root = Tk()

    modelo = Modelo(DB)
    controlador = Controlador(modelo)
    vista = Vista(root, controlador)
