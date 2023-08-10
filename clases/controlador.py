"""
Controlador:
    Administra el flujo de ejecución principal de nuestra aplicación. 
"""


class Controlador:
    def __init__(self, modelo):
        self.modelo = modelo

    def alta(self, variables_de_control):
        nombre = variables_de_control["nombre"].get()
        autor = variables_de_control["autor"].get()
        editorial = variables_de_control["editorial"].get()
        año = variables_de_control["año"].get()
        categoria = variables_de_control["categoria"].get()
        estado = variables_de_control["estado"].get()
        self.modelo.alta_db(nombre, autor, editorial, año, categoria, estado)

    def baja(self, id):
        self.modelo.baja_db(id.get())

    def modificar(self, variables_de_control):
        id = variables_de_control["id"].get()
        nombre = variables_de_control["nombre"].get()
        autor = variables_de_control["autor"].get()
        editorial = variables_de_control["editorial"].get()
        año = variables_de_control["año"].get()
        categoria = variables_de_control["categoria"].get()
        estado = variables_de_control["estado"].get()
        self.modelo.modificar_db(id, nombre, autor, editorial, año, categoria, estado)

    def consultar(self, sobre, clausula, df=True):
        return self.modelo.consultar_db(sobre, clausula, df)

    def agregar_observador(self, observador):
        self.modelo.observadores.append(observador)
