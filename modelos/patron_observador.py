from modelos.registro_de_logs import Logueador


class Sujeto:
    observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def eliminar_observador(self, observador):
        self.observadores.pop(observador)

    def notificar_a_observadores(self):
        for observador in self.observadores:
            observador.darse_por_notificado()


class ObservadorABS:
    def darse_por_notificado(self):
        raise NotImplementedError("Método 'darse_por_notificado()' no implementado")
