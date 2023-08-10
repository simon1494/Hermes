from modelos.registro_de_logs import Logueador


class Sujeto:
    observadores = []

    def agregar(self, observador):
        self.observadores.append(observador)

    def eliminar(self, observador):
        self.observadores.pop(observador)

    def notificar_operacion_en_base(self, tipo_de_operacion):
        for observador in self.observadores:
            observador.notificarse(tipo_de_operacion)


class ObservadorABS:
    def notificarse(self, tipo_de_operacion):
        raise NotImplementedError("Método 'darse_por_notificado()' no implementado")


class ObservadorIMP(ObservadorABS, Logueador):
    def __init__(self, objeto_observado):
        self.objeto_observado = objeto_observado
        self.objeto_observado.agregar(self)

    def notificarse(self, tipo_de_operacion):
        logger = Logueador()
        logger.loguear(tipo_de_operacion)
