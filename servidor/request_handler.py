from socketserver import BaseRequestHandler
from datetime import datetime
from pickle import loads


class Requesteador(BaseRequestHandler):
    def handle(self):
        self.recibir_paquete_y_generar_atributos_de_instancia()
        self.procesar_paquete_del_cliente()
        self.responder_a_cliente()

    def recibir_paquete_y_generar_atributos_de_instancia(self):
        print("Recibiendo paquete...")
        self.data_recibida = loads(self.request[0])
        self.tipo_de_operacion = self.data_recibida[0]
        self.datos_de_la_operacion = self.data_recibida[1]
        self.socket = self.request[1]
        self.estampa_temporal_de_operacion = datetime.now().strftime("%Y/%m/%d")
        self.preparar_respuesta()

    def preparar_respuesta(self):
        print("Preparando respuesta...")
        a = self.estampa_temporal_de_operacion
        b = self.elegir_respuesta_segun_operacion()
        c = self.datos_de_la_operacion
        self.respuesta = f"{a} - {b} - {c}"

    def elegir_respuesta_segun_operacion(self):
        if self.tipo_de_operacion == "alta":
            return "Se procesó operacion de alta"
        elif self.tipo_de_operacion == "baja":
            return "Se procesó operacion de baja"
        elif self.tipo_de_operacion == "modificacion":
            return "Se procesó operacion de modificacion"
        elif self.tipo_de_operacion == "consulta":
            return "Se procesó operacion de consulta"

    def procesar_paquete_del_cliente(self):
        print("Procesando paquete...")
        print(self.data_recibida[1])

    def responder_a_cliente(self):
        self.socket.sendto(self.respuesta.encode("UTF-8"), self.client_address)
        print("Respuesta enviada")
