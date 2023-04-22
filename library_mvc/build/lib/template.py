import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import model

#:::::::::::::::Seteo general de la ventana. Creación y posicionamiento de widgets::::::::::::
def app():

    mensaje_error = (
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

    ventana = tk.Tk()
    ventana.title("Hermes BookSearch 1.0")
    ventana.config(bg="#091430")
    ventana.geometry(model.__center_window__(ventana, 700, 750))

    #::::::::::::::Variables de control para la manipulación de los campos de Data Entry::::::::::

    control_id = tk.StringVar()
    control_nombre = tk.StringVar()
    control_autor = tk.StringVar()
    control_editorial = tk.StringVar()
    control_año = tk.StringVar()
    control_categoria = tk.StringVar()
    control_estado = tk.StringVar()
    control_consulta = tk.StringVar()

    control_id.set("")
    control_nombre.set("")
    control_autor.set("")
    control_editorial.set("")
    control_año.set("")
    control_categoria.set("")
    control_estado.set("")
    control_consulta.set("")

    #:::::::::::::::::::::::::::::::::::::::::::LABELS::::::::::::::::::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::Etiquetas de los campos de Data Entry:::::::::::::::::::::::::::

    fuente = Font(family="Consolas", size=12, weight="bold")
    s = ttk.Style(ventana)
    s.configure("TLabel", background="#091430", foreground="white")

    lb_id = ttk.Label(ventana, text="ID", anchor=tk.E, style="TLabel", font=fuente)
    lb_nombre = ttk.Label(
        ventana, text="Nombre", anchor=tk.E, style="TLabel", font=fuente
    )
    lb_autor = ttk.Label(
        ventana, text="Autor", anchor=tk.E, style="TLabel", font=fuente
    )
    lb_editorial = ttk.Label(
        ventana, text="Editorial", anchor=tk.E, style="TLabel", font=fuente
    )
    lb_año = ttk.Label(
        ventana, text="Año publicación", anchor=tk.E, style="TLabel", font=fuente
    )
    lb_categoria = ttk.Label(
        ventana, text="Categoría", anchor=tk.E, style="TLabel", font=fuente
    )
    lb_estado = ttk.Label(
        ventana, text="Estado", anchor=tk.E, style="TLabel", font=fuente
    )

    lb_id.place(x=82, y=28, width=103, height=30)
    lb_nombre.place(x=82, y=73, width=103, height=30)
    lb_autor.place(x=82, y=118, width=103, height=30)
    lb_editorial.place(x=82, y=163, width=103, height=30)
    lb_año.place(x=18, y=208, width=167, height=30)
    lb_categoria.place(x=92, y=253, width=93, height=30)
    lb_estado.place(x=92, y=298, width=93, height=30)

    #:::::::::::::::::::::::::::::::::::ENTRIES & COMBOBOXES::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::Entries y Comboboxes de los campos de Data Entry:::::::::::::::::::::::

    box_id = tk.Entry(
        ventana, textvariable=control_id, bg="#A5FFCE", font=("Consolas 11")
    )
    box_nombre = tk.Entry(
        ventana, textvariable=control_nombre, bg="#A5FFCE", font=("Consolas 11")
    )
    box_autor = tk.Entry(
        ventana, textvariable=control_autor, bg="#A5FFCE", font=("Consolas 11")
    )
    box_editorial = tk.Entry(
        ventana, textvariable=control_editorial, bg="#A5FFCE", font=("Consolas 11")
    )
    box_año = tk.Entry(
        ventana, textvariable=control_año, bg="#A5FFCE", font=("Consolas 11")
    )
    box_categoria = ttk.Combobox(
        ventana,
        textvariable=control_categoria,
        values=("Ficción", "Ensayo", "Poesía", "Filosofía", "Sociología", "Otros"),
    )
    box_estado = ttk.Combobox(
        ventana, textvariable=control_estado, values=("En Biblioteca", "Prestado")
    )
    box_consulta = ttk.Combobox(
        ventana,
        textvariable=control_consulta,
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

    box_id.place(x=203, y=28, width=100, height=30)
    box_nombre.place(x=203, y=73, width=300, height=30)
    box_autor.place(x=203, y=118, width=230, height=30)
    box_editorial.place(x=203, y=163, width=230, height=30)
    box_año.place(x=203, y=208, width=100, height=30)
    box_categoria.place(x=203, y=253, width=230, height=30)
    box_estado.place(x=203, y=298, width=130, height=30)

    #::::::::::::::::::::Botonera general para interacción con el usuario:::::::::::::::::::::::::

    bt_agregar = tk.Button(
        ventana,
        text="Añadir",
        background="#02FF3A",
        activebackground="#751C3C",
        font=("Consolas 12 bold"),
        command=lambda: model.agregar_libro(
            control_id,
            control_nombre,
            control_autor,
            control_editorial,
            control_año,
            control_categoria,
            control_estado,
            mensaje_error,
            tree,
        ),
    )
    bt_eliminar = tk.Button(
        ventana,
        text="Eliminar",
        background="#02FF3A",
        activebackground="#751C3C",
        font=("Consolas 12 bold"),
        command=lambda: model.eliminar_libro(
            control_id,
            control_nombre,
            control_autor,
            control_editorial,
            control_año,
            control_categoria,
            control_estado,
            mensaje_error,
            tree,
        ),
    )
    bt_modificar = tk.Button(
        ventana,
        text="Modificar",
        background="#02FF3A",
        activebackground="#751C3C",
        font=("Consolas 12 bold"),
        command=lambda: model.modificar_libro(
            control_id,
            control_nombre,
            control_autor,
            control_editorial,
            control_año,
            control_categoria,
            control_estado,
            mensaje_error,
            tree,
        ),
    )
    bt_consultar = tk.Button(
        ventana,
        text="Consultar",
        background="#02FF3A",
        activebackground="#751C3C",
        font=("Consolas 12 bold"),
        command=lambda: model.consultar(
            control_consulta,
            control_id,
            control_nombre,
            control_autor,
            control_editorial,
            control_año,
            control_categoria,
            control_estado,
            mensaje_error,
            tree,
        ),
    )

    bt_agregar.place(x=25, y=370, width=136, height=36)
    bt_eliminar.place(x=196, y=370, width=136, height=36)
    bt_modificar.place(x=367, y=370, width=136, height=36)
    bt_consultar.place(x=538, y=370, width=136, height=36)

    #::::::::::::::::Treeview donde se visualizan los datos de las consultas a DB:::::::::::::::::

    columnas = ("id", "nombre", "autor", "editorial", "categoria", "estado")
    tree = ttk.Treeview(ventana, columns=columnas)
    tree.heading("id", text="id")
    tree.heading("nombre", text="Nombre")
    tree.heading("autor", text="Autor")
    tree.heading("editorial", text="Editorial")
    tree.heading("categoria", text="Categoría")
    tree.heading("estado", text="Estado")
    tree.place(x=20, y=427, width=660, height=300)
    tree.column("#0", minwidth=0, width=0, anchor="center")
    tree.column("id", minwidth=0, width=0, anchor="center")
    tree.column("nombre", minwidth=0, width=220, anchor="center")
    tree.column("autor", minwidth=0, width=110, anchor="center")
    tree.column("editorial", minwidth=0, width=110, anchor="center")
    tree.column("categoria", minwidth=0, width=110, anchor="center")
    tree.column("estado", minwidth=0, width=110, anchor="center")
    tree.bind(
        "<ButtonRelease-1>",
        lambda evento: model.select_item(
            a=tree,
            b=control_id,
            c=control_nombre,
            d=control_autor,
            e=control_editorial,
            f=control_año,
            g=control_categoria,
            h=control_estado,
        ),
    )

    model.__built__(tree)

    ventana.mainloop()
