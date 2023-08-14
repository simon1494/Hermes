from request_handler import Requesteador
from socketserver import UDPServer


HOST = "localhost"
PORT = 9999

with UDPServer((HOST, PORT), Requesteador) as server:
    print("Servidor UP")
    server.serve_forever()
