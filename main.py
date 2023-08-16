import sys

sys.path.append("../library")

if __name__ == "__main__":
    import threading
    import subprocess
    import os
    from tkinter import Tk
    from clases.logo_inicio import LogoInicio
    from modelo import Modelo
    from vista import Vista
    from clases.controlador import Controlador
    from clases.estructura_base import DB

    def lanzar_servidor():
        global SERVIDOR
        ruta_servidor = os.path.dirname(os.path.abspath(__file__))
        SERVIDOR = subprocess.Popen(
            [
                sys.executable,
                rf"{ruta_servidor}\controlador_servidor.py",
            ]
        )
        SERVIDOR.communicate()

    def lanzar_inicio():
        logueo = LogoInicio()

    HOST = "localhost"
    PORT = 9999

    # LANZA HILO QUE ENCIENDE EL SERVIDOR Y LO MANTIENE A LA ESCUCHA
    hilo_servidor = threading.Thread(target=lanzar_servidor)
    hilo_servidor.start()

    # LANZA HILO QUE MUESTRA EL LOGO DE INICIO. 6 SEGUNDOS DESPUES SE LANZA EL HILO PRINCIPAL
    hilo_inicio = threading.Thread(target=lanzar_inicio)
    hilo_inicio.start()
    hilo_inicio.join()

    root = Tk()

    modelo = Modelo(DB, (HOST, PORT))
    controlador = Controlador(modelo)
    vista = Vista(root, controlador)

    # CONTROLA APAGADO DEL SERVIDOR LUEGO DE LA DESTRUCCIÓN DE LA APP
    if hilo_servidor.is_alive():
        print("Apagando servidor...")
        SERVIDOR.kill()
        print("Servidor apagado.")
