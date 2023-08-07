from tkinter.messagebox import showinfo
from tkinter.messagebox import showwarning
from tkinter.messagebox import showerror
from tkinter.messagebox import askyesno

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
        respuesta = askyesno(title="¿Desea...?",message=mensaje)
        return respuesta