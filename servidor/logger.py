import os


class Logger:
    def __init__(self):
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        self.filename = f"{ruta_actual}\log_servidor.log"

    def log(self, message):
        with open(self.filename, "a") as file:
            file.write(message + "\n")
