from tkinter.messagebox import showinfo
from tkinter.messagebox import showwarning
from tkinter.messagebox import showerror
from tkinter.messagebox import askyesno


def mensaje_operacion(tipo_operacion):
    def _mensaje_operacion(funcion):
        def envoltura(*args, **kwargs):
            if tipo_operacion == "alta":
                try:
                    funcion(*args, **kwargs)
                    showinfo(
                        title="Aviso de alta",
                        message="El libro fue ingresado correctamente",
                    )
                except Exception as error:
                    showerror(
                        title="Error en alta",
                        message=f"Se registro un error durante el alta: {error}",
                    )
            if tipo_operacion == "baja":
                try:
                    funcion(*args, **kwargs)
                    showinfo(
                        title="Aviso de baja",
                        message="El libro fue eliminado correctamente",
                    )
                except Exception as error:
                    showerror(
                        title="Error en baja",
                        message=f"Se registro un error durante la baja: {error}",
                    )
            if tipo_operacion == "mod":
                try:
                    funcion(*args, **kwargs)
                    showinfo(
                        title="Aviso de modificacion",
                        message="El libro fue modificado correctamente",
                    )
                except Exception as error:
                    showerror(
                        title="Error en modificación",
                        message=f"Se registro un error durante la modificación: {error}",
                    )

        return envoltura

    return _mensaje_operacion


class Mensajes:
    @staticmethod
    def mostrar_mensaje_info(mensaje):
        showinfo(title="Aviso", message=mensaje)

    @staticmethod
    def mostrar_mensaje_advertencia(mensaje):
        showwarning(title="Advertencia", message=mensaje)

    @staticmethod
    def mostrar_mensaje_error(mensaje):
        showerror(title="Error", message=mensaje)

    @staticmethod
    def mostrar_pregunta_si_o_no(mensaje):
        respuesta = askyesno(title="¿Desea...?", message=mensaje)
        return respuesta
