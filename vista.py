import sys

sys.path.append("../library")
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter.ttk import Style
from clases.patron_observador import ObservadorABS
from clases.modelos_vista import VentanaConfig
from clases.modelos_vista import Boton
from clases.modelos_vista import Etiqueta
from clases.modelos_vista import EntradaTexto
from clases.operaciones_widgets import WidgetOps

"""
Vista:
    Administra la interfaz de nuestra aplicación. 
"""


class Vista(VentanaConfig, WidgetOps, ObservadorABS):
    """
    Estructura la interfaz gráfica, a la vez que incorpora todas las funcionalidades y lógica interna del programa, así como tambien conexión con la base de datos, al heredar de la clase model.Api
    """

    def __init__(self, win, objeto_observado):
        # Agrego la VISTA al listado de observadores del MODELO
        self.objeto_observado = objeto_observado
        self.objeto_observado.agregar_observador(self)

        self.ventana = win
        self.ventana.title("Proyecto Hermes")
        self.ventana.geometry(self.centrar_ventana(700, 750))
        self.crear_todo()

    def crear_variables_control(self):
        """
        Crea las variables de control utilizadas para manipular a través de la aplicación la información de los registros.
        """

        self.control_id = tk.StringVar()
        self.control_nombre = tk.StringVar()
        self.control_autor = tk.StringVar()
        self.control_editorial = tk.StringVar()
        self.control_anio = tk.StringVar()
        self.control_categoria = tk.StringVar()
        self.control_estado = tk.StringVar()
        self.control_consulta = tk.StringVar()

        self.variables_de_control = {
            "id": self.control_id,
            "nombre": self.control_nombre,
            "autor": self.control_autor,
            "editorial": self.control_editorial,
            "año": self.control_anio,
            "categoria": self.control_categoria,
            "estado": self.control_estado,
            "consulta": self.control_consulta,
        }

        self.control_id.set("")
        self.control_nombre.set("")
        self.control_autor.set("")
        self.control_editorial.set("")
        self.control_anio.set("")
        self.control_categoria.set("")
        self.control_estado.set("")
        self.control_consulta.set("")

    def crear_estilos_y_fuentes(self):
        """Crea estilos y fuentes utilizados por la interfaz gráfica"""

        self.ESTILO_ETIQUETAS = Style(self.ventana)
        self.ESTILO_ETIQUETAS.configure(
            "TLabel",
            background=self.COLOR_DE_FONDO_ETIQUETAS,
            foreground=self.COLOR_DE_TEXTO_ETIQUETAS,
        )
        self.FUENTE = Font(family="Consolas", size=12, weight="bold")
        self.FUENTE_CHICA = Font(family="Consolas", size=9, weight="bold")
        self.ventana.config(bg=self.COLOR_DE_FONDO)

    def crear_labels(self):
        """Crea las etiquetas de los data entries."""

        self.lb_id = Etiqueta(self.ventana, text="ID", font=self.FUENTE, style="TLabel")
        self.lb_id_info = Etiqueta(
            self.ventana,
            text="(Usar solo para Eliminar, Modificar o Consultar)",
            anchor=tk.W,
            font=self.FUENTE_CHICA,
            style="TLabel",
        )

        self.lb_nombre = Etiqueta(
            self.ventana, text="Nombre", font=self.FUENTE, style="TLabel"
        )
        self.lb_autor = Etiqueta(
            self.ventana, text="Autor", font=self.FUENTE, style="TLabel"
        )
        self.lb_editorial = Etiqueta(
            self.ventana, text="Editorial", font=self.FUENTE, style="TLabel"
        )
        self.lb_anio = Etiqueta(
            self.ventana, text="Año de publicación", font=self.FUENTE, style="TLabel"
        )
        self.lb_categoria = Etiqueta(
            self.ventana, text="Categoría", font=self.FUENTE, style="TLabel"
        )
        self.lb_estado = Etiqueta(
            self.ventana, text="Estado", font=self.FUENTE, style="TLabel"
        )

        self.lb_id.place(x=82, y=28, width=103, height=30)
        self.lb_id_info.place(x=310, y=28, width=400, height=30)
        self.lb_nombre.place(x=82, y=73, width=103, height=30)
        self.lb_autor.place(x=82, y=118, width=103, height=30)
        self.lb_editorial.place(x=82, y=163, width=103, height=30)
        self.lb_anio.place(x=18, y=208, width=167, height=30)
        self.lb_categoria.place(x=92, y=253, width=93, height=30)
        self.lb_estado.place(x=92, y=298, width=93, height=30)

    def crear_entries(self):
        """Crea los widgets de entrada de texto con los que el usuario interactuará para cargar información"""

        self.box_id = EntradaTexto(
            self.ventana,
            textvariable=self.control_id,
            bg="#FAC921",
        )
        self.box_nombre = EntradaTexto(
            self.ventana,
            textvariable=self.control_nombre,
        )
        self.box_autor = EntradaTexto(
            self.ventana,
            textvariable=self.control_autor,
        )
        self.box_editorial = EntradaTexto(
            self.ventana,
            textvariable=self.control_editorial,
        )
        self.box_anio = EntradaTexto(
            self.ventana,
            textvariable=self.control_anio,
        )

        self.box_id.place(x=203, y=28, width=100, height=30)
        self.box_nombre.place(x=203, y=73, width=300, height=30)
        self.box_autor.place(x=203, y=118, width=230, height=30)
        self.box_editorial.place(x=203, y=163, width=230, height=30)
        self.box_anio.place(x=203, y=208, width=100, height=30)

    def crear_combo_boxes(self):
        """Crea los listados seleccionable con los que el usuario interactuará."""

        self.box_categoria = ttk.Combobox(
            self.ventana,
            textvariable=self.control_categoria,
            values=("Ficción", "Ensayo", "Poesía", "Filosofía", "Sociología", "Otros"),
            state="readonly",
        )
        self.box_estado = ttk.Combobox(
            self.ventana,
            textvariable=self.control_estado,
            values=("En Biblioteca", "Prestado"),
            state="readonly",
        )
        self.box_consulta = ttk.Combobox(
            self.ventana,
            textvariable=self.control_consulta,
            values=(
                "Ver todo",
                "Buscar id",
                "Buscar nombre",
                "Buscar autor",
                "Buscar editorial",
                "Buscar anio",
                "Buscar categoria",
                "Buscar estado",
            ),
            state="readonly",
        )

        self.box_categoria.place(x=203, y=253, width=230, height=30)
        self.box_estado.place(x=203, y=298, width=130, height=30)
        self.box_consulta.place(x=538, y=325, width=136, height=30)

    def crear_botones(self):
        """Crea los botones de nuestra aplicación."""

        self.bt_agregar = Boton(
            master=self.ventana,
            text="Añadir",
            background="#22DB68",
            command=lambda: self.alta(),
        )
        self.bt_eliminar = Boton(
            master=self.ventana, text="Eliminar", command=lambda: self.baja()
        )
        self.bt_modificar = Boton(
            master=self.ventana, text="Modificar", command=lambda: self.modificar()
        )
        self.bt_consultar = Boton(
            master=self.ventana, text="Consultar", command=lambda: self.consultar()
        )

        self.bt_agregar.place(x=25, y=370, width=136, height=36)
        self.bt_eliminar.place(x=196, y=370, width=136, height=36)
        self.bt_modificar.place(x=367, y=370, width=136, height=36)
        self.bt_consultar.place(x=538, y=370, width=136, height=36)

    def crear_y_armar_treeview(self):
        """Crea el Treeview de nuestra aplicación y lo arma con la información que existe en base."""

        columnas = ("id", "nombre", "autor", "editorial", "categoria", "estado")
        self.tree = ttk.Treeview(self.ventana, columns=columnas)
        self.tree.heading("id", text="id")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("autor", text="Autor")
        self.tree.heading("editorial", text="Editorial")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("estado", text="Estado")
        self.tree.place(x=20, y=427, width=660, height=300)
        self.tree.column("#0", minwidth=0, width=0, anchor="center")
        self.tree.column("id", minwidth=0, width=0, anchor="center")
        self.tree.column("nombre", minwidth=0, width=220, anchor="center")
        self.tree.column("autor", minwidth=0, width=110, anchor="center")
        self.tree.column("editorial", minwidth=0, width=110, anchor="center")
        self.tree.column("categoria", minwidth=0, width=110, anchor="center")
        self.tree.column("estado", minwidth=0, width=110, anchor="center")
        self.tree.bind(
            "<ButtonRelease-1>",
            lambda evento: self.seleccionar_item(self.tree, self.variables_de_control),
        )
        self.armar_treeview(self.tree)

    def crear_todo(self):
        self.crear_variables_control()
        self.crear_estilos_y_fuentes()
        self.crear_labels()
        self.crear_entries()
        self.crear_botones()
        self.crear_combo_boxes()
        self.crear_y_armar_treeview()
        self.correr()

    def alta(self):
        if self.validar_entradas(self.variables_de_control):
            self.objeto_observado.alta(self.variables_de_control)

    def baja(self):
        if self.mostrar_pregunta_si_o_no("¿Realmente desea eliminar este libro?"):
            if self.validar_id(self.control_id):
                self.objeto_observado.baja(self.control_id)
            else:
                self.mostrar_mensaje_advertencia(
                    f"El ID ingresado no es válido para ejecutar la acción."
                )

    def modificar(self):
        if self.mostrar_pregunta_si_o_no("¿Realmente desea modificar este libro?"):
            if self.validar_entradas(self.variables_de_control):
                self.objeto_observado.modificar(self.variables_de_control)
            else:
                self.mostrar_mensaje_advertencia(
                    f"Controle que todos los campos contengan datos válidos"
                )

    def consultar(self):
        sobre, clausula = self.armar_consulta(
            self.variables_de_control, self.MENSAJE_DE_ERROR
        )
        self.limpiar_treeview(self.tree)
        self.armar_treeview(self.tree, sobre, clausula)

    def notificarse(self):
        self.limpiar_y_armar(self.tree)
        self.blanquear_entradas(self.variables_de_control)

    def correr(self):
        """Inicia el loop de nuestra interfaz gráfica."""
        self.ventana.mainloop()
