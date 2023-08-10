from screeninfo import get_monitors
import tkinter
from tkinter import Button
from tkinter import Entry
from tkinter.ttk import Label


class MetodosBaseVentanas:
    @staticmethod
    def centrar_ventana(window_width, window_heigth):
        monitores = get_monitors()
        if monitores:
            primer_monitor = monitores[0]
            screen_width = primer_monitor.width
            screen_heigth = primer_monitor.height
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_heigth / 2 - window_heigth / 2)
        return f"{window_width}x{window_heigth}+{center_x}+{center_y}"


class VentanaConfig(MetodosBaseVentanas):
    COLOR_DE_FONDO = "#091430"
    COLOR_DE_FONDO_ETIQUETAS = "#091430"
    COLOR_DE_TEXTO_ETIQUETAS = "white"
    MENSAJE_DE_ERROR = (
        "\n\n"
        + "Tenga en cuenta:"
        + "\n\n"
        + "ID: debe ser un número entero"
        + "\n"
        + "Nombre: No debe contener caracteres especiales ni abreviatuas"
        + "\n"
        + "Autor: No debe contener números ni caracteres especiales"
        + "\n"
        + "Editorial: No debe contener carateres especiales"
        + "\n"
        + "año: Debe ser un numero entero entre 1900 y 2029"
        + "\n"
        + "Categoría: Debe estar entre los items de la lista desplegable"
        + "\n"
        + "Estado: Debe estar entre los items de la lista desplegable"
    )


class Boton(Button):
    COLOR = "#FAC921"
    COLOR_AL_ACTIVAR = "#751C3C"
    FUENTE = "Consolas 12 bold"

    def __init__(self, master=None, background=COLOR, **kwargs):
        super().__init__(
            master,
            background=background,
            activebackground=self.COLOR_AL_ACTIVAR,
            font=self.FUENTE,
            **kwargs,
        )


class Etiqueta(Label):
    ANCHOR = (tkinter.E,)

    def __init__(self, master=None, anchor=ANCHOR, **kwargs):
        super().__init__(
            master,
            anchor=anchor,
            **kwargs,
        )


class EntradaTexto(Entry):
    COLOR_DE_FONDO = "#A5FFCE"
    FUENTE = "Consolas 11"

    def __init__(self, master=None, bg=COLOR_DE_FONDO, **kwargs):
        super().__init__(
            master,
            font=self.FUENTE,
            bg=bg,
            **kwargs,
        )


class EntryB(Entry):
    ...
