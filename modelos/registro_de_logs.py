import logging
import os
import datetime


class Logueador:
    def __init__(self, tipo_de_operacion):
        CARPETA_DEL_ARCHIVO_LOGS = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../")
        )
        ARCHIVO_LOGS = f"{CARPETA_DEL_ARCHIVO_LOGS}/logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

        logging.basicConfig(
            filename=ARCHIVO_LOGS,
            level=logging.DEBUG,
            format="%(asctime)s:   %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )

    def loguear(self, tipo_de_operacion):
        if tipo_de_operacion == "alta":
            logging.info("Se realizó operacion de alta")
        if tipo_de_operacion == "baja":
            logging.info("Se realizó operacion de baja")
        if tipo_de_operacion == "mod":
            logging.info("Se realizó operacion de modificación")
        if tipo_de_operacion == "con":
            logging.info("Se realizó operacion de consulta")
