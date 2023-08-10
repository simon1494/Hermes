class Sujeto:
    observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def eliminar_observador(self, observador):
        self.observadores.pop(observador)

    def notificar_a_observadores(self):
        for observador in self.observadores:
            observador.notificarse()


class ObservadorABS:
    def notificarse(self):
        raise NotImplementedError("Método 'notificarse()' no implementado")
