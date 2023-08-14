import socket
from pickle import dumps


class Cliente:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def enviar_info_y_procesar_respuesta(self, tipo_de_operacion, info):
        info_a_enviar = self.preparar_info_a_enviar(tipo_de_operacion, info)
        self.sock.sendto(info_a_enviar, (self.HOST, self.PORT))
        received = self.sock.recvfrom(1024)
        # print(received[0].decode("UTF-8"))

    def preparar_info_a_enviar(self, tipo_de_operacion, info):
        return dumps([tipo_de_operacion, info])
