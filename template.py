import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from model import Api


class App(Api):
    def __init__(self, win):

        self.crear_db()

        self.mensaje_error = (
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
            + "Año: Debe ser un numero entero entre 1900 y 2029"
            + "\n"
            + "Categoría: Debe estar entre los items de la lista desplegable"
            + "\n"
            + "Estado: Debe estar entre los items de la lista desplegable"
        )

        self.ventana = win
        self.ventana.title("Hermes BookSearch 1.0")
        self.ventana.config(bg="#091430")
        self.ventana.geometry(self.centrar_ventana(self.ventana, 700, 750))

        #::::::::::::::Variables de control para la manipulación de los campos de Data Entry::::::::::

        self.control_id = tk.StringVar()
        self.control_nombre = tk.StringVar()
        self.control_autor = tk.StringVar()
        self.control_editorial = tk.StringVar()
        self.control_año = tk.StringVar()
        self.control_categoria = tk.StringVar()
        self.control_estado = tk.StringVar()
        self.control_consulta = tk.StringVar()

        self.control_id.set("")
        self.control_nombre.set("")
        self.control_autor.set("")
        self.control_editorial.set("")
        self.control_año.set("")
        self.control_categoria.set("")
        self.control_estado.set("")
        self.control_consulta.set("")

        #:::::::::::::::::::::::::::::::::::::::::::LABELS::::::::::::::::::::::::::::::::::::::::::::
        #:::::::::::::::::::::::::::::Etiquetas de los campos de Data Entry:::::::::::::::::::::::::::

        self.fuente = Font(family="Consolas", size=12, weight="bold")
        self.fuente1 = Font(family="Consolas", size=9, weight="bold")

        self.s = ttk.Style(self.ventana)
        self.s.configure("TLabel", background="#091430", foreground="white")

        self.lb_id = ttk.Label(
            self.ventana, text="ID", anchor=tk.E, style="TLabel", font=self.fuente
        )
        self.lb_id_info = ttk.Label(
            self.ventana,
            text="(Usar solo para Eliminar, Modificar o Consultar)",
            anchor=tk.W,
            style="TLabel",
            font=self.fuente1,
        )

        self.lb_nombre = ttk.Label(
            self.ventana, text="Nombre", anchor=tk.E, style="TLabel", font=self.fuente
        )
        self.lb_autor = ttk.Label(
            self.ventana, text="Autor", anchor=tk.E, style="TLabel", font=self.fuente
        )
        self.lb_editorial = ttk.Label(
            self.ventana,
            text="Editorial",
            anchor=tk.E,
            style="TLabel",
            font=self.fuente,
        )
        self.lb_año = ttk.Label(
            self.ventana,
            text="Año publicación",
            anchor=tk.E,
            style="TLabel",
            font=self.fuente,
        )
        self.lb_categoria = ttk.Label(
            self.ventana,
            text="Categoría",
            anchor=tk.E,
            style="TLabel",
            font=self.fuente,
        )
        self.lb_estado = ttk.Label(
            self.ventana, text="Estado", anchor=tk.E, style="TLabel", font=self.fuente
        )

        self.lb_id.place(x=82, y=28, width=103, height=30)
        self.lb_id_info.place(x=310, y=28, width=400, height=30)
        self.lb_nombre.place(x=82, y=73, width=103, height=30)
        self.lb_autor.place(x=82, y=118, width=103, height=30)
        self.lb_editorial.place(x=82, y=163, width=103, height=30)
        self.lb_año.place(x=18, y=208, width=167, height=30)
        self.lb_categoria.place(x=92, y=253, width=93, height=30)
        self.lb_estado.place(x=92, y=298, width=93, height=30)

        #:::::::::::::::::::::::::::::::::::ENTRIES & COMBOBOXES::::::::::::::::::::::::::::::::::::::
        #::::::::::::::::::::::Entries y Comboboxes de los campos de Data Entry:::::::::::::::::::::::

        self.box_id = tk.Entry(
            self.ventana,
            textvariable=self.control_id,
            bg="#FAC921",
            font=("Consolas 11"),
        )
        self.box_nombre = tk.Entry(
            self.ventana,
            textvariable=self.control_nombre,
            bg="#A5FFCE",
            font=("Consolas 11"),
        )
        self.box_autor = tk.Entry(
            self.ventana,
            textvariable=self.control_autor,
            bg="#A5FFCE",
            font=("Consolas 11"),
        )
        self.box_editorial = tk.Entry(
            self.ventana,
            textvariable=self.control_editorial,
            bg="#A5FFCE",
            font=("Consolas 11"),
        )
        self.box_año = tk.Entry(
            self.ventana,
            textvariable=self.control_año,
            bg="#A5FFCE",
            font=("Consolas 11"),
        )
        self.box_categoria = ttk.Combobox(
            self.ventana,
            textvariable=self.control_categoria,
            values=("Ficción", "Ensayo", "Poesía", "Filosofía", "Sociología", "Otros"),
        )
        self.box_estado = ttk.Combobox(
            self.ventana,
            textvariable=self.control_estado,
            values=("En Biblioteca", "Prestado"),
        )
        box_consulta = ttk.Combobox(
            self.ventana,
            textvariable=self.control_consulta,
            values=(
                "Ver todo",
                "Buscar id",
                "Buscar nombre",
                "Buscar autor",
                "Buscar editorial",
                "Buscar año",
                "Buscar categoria",
                "Buscar estado",
            ),
            state="readonly",
        )
        box_consulta.place(x=538, y=325, width=136, height=30)

        self.box_id.place(x=203, y=28, width=100, height=30)
        self.box_nombre.place(x=203, y=73, width=300, height=30)
        self.box_autor.place(x=203, y=118, width=230, height=30)
        self.box_editorial.place(x=203, y=163, width=230, height=30)
        self.box_año.place(x=203, y=208, width=100, height=30)
        self.box_categoria.place(x=203, y=253, width=230, height=30)
        self.box_estado.place(x=203, y=298, width=130, height=30)

        #::::::::::::::::::::Botonera general para interacción con el usuario:::::::::::::::::::::::::

        self.bt_agregar = tk.Button(
            self.ventana,
            text="Añadir",
            background="#22DB68",
            activebackground="#751C3C",
            font=("Consolas 12 bold"),
            command=lambda: self.agregar_libro(
                self.control_id,
                self.control_nombre,
                self.control_autor,
                self.control_editorial,
                self.control_año,
                self.control_categoria,
                self.control_estado,
                self.mensaje_error,
                self.tree,
            ),
        )
        self.bt_eliminar = tk.Button(
            self.ventana,
            text="Eliminar",
            background="#FAC921",
            activebackground="#751C3C",
            font=("Consolas 12 bold"),
            command=lambda: self.eliminar_libro(
                self.control_id,
                self.control_nombre,
                self.control_autor,
                self.control_editorial,
                self.control_año,
                self.control_categoria,
                self.control_estado,
                self.mensaje_error,
                self.tree,
            ),
        )
        self.bt_modificar = tk.Button(
            self.ventana,
            text="Modificar",
            background="#FAC921",
            activebackground="#751C3C",
            font=("Consolas 12 bold"),
            command=lambda: self.modificar_libro(
                self.control_id,
                self.control_nombre,
                self.control_autor,
                self.control_editorial,
                self.control_año,
                self.control_categoria,
                self.control_estado,
                self.mensaje_error,
                self.tree,
            ),
        )
        self.bt_consultar = tk.Button(
            self.ventana,
            text="Consultar",
            background="#FAC921",
            activebackground="#751C3C",
            font=("Consolas 12 bold"),
            command=lambda: self.consultar(
                self.control_consulta,
                self.control_id,
                self.control_nombre,
                self.control_autor,
                self.control_editorial,
                self.control_año,
                self.control_categoria,
                self.control_estado,
                self.mensaje_error,
                self.tree,
            ),
        )

        self.bt_agregar.place(x=25, y=370, width=136, height=36)
        self.bt_eliminar.place(x=196, y=370, width=136, height=36)
        self.bt_modificar.place(x=367, y=370, width=136, height=36)
        self.bt_consultar.place(x=538, y=370, width=136, height=36)

        #::::::::::::::::Treeview donde se visualizan los datos de las consultas a DB:::::::::::::::::

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
            lambda evento: self.seleccionar_item(
                a=self.tree,
                b=self.control_id,
                c=self.control_nombre,
                d=self.control_autor,
                e=self.control_editorial,
                f=self.control_año,
                g=self.control_categoria,
                h=self.control_estado,
            ),
        )

        self.armar_treeview(self.tree)
