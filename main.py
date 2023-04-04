import tkinter as tk
import pandas as pd
import sqlite3
import re
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.font import Font

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::DATABASE FUNCTIONS::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Comprueba si existe una base de datos y, en caso de no existir, la crea.
def create_db():
    conn = sqlite3.connect("biblioteca")
    c = conn.cursor()

    c.execute(
        """
                Create TABLE IF NOT EXISTS [libros]
                ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [nombre] TEXT,
                [autor] TEXT,
                [editorial] DATE,
                [año] TIME,
                [categoria] TEXT,
                [estado] TEXT)
                """
    )
    conn.commit()


# Envía una consulta INSERT a la DB con los datos ingresados por el usuario.
def insert_item(nombre, autor, editorial, año, categoria, estado):
    conn = sqlite3.connect("biblioteca")
    c = conn.cursor()

    c.execute(
        f"""
                INSERT INTO libros 
                (nombre, autor, editorial, año, categoria, estado) 
                VALUES ("{nombre}", "{autor}", "{editorial}", 
                "{año}", "{categoria}", "{estado}")
                """
    )
    conn.commit()


# Envía una consulta DELETE a la DB con el id del item facilitado por el usuario.
def delete_item(id):
    conn = sqlite3.connect("biblioteca")
    c = conn.cursor()

    c.execute(
        f"""
                    DELETE FROM libros
                    WHERE id={id}
                    """
    )
    conn.commit()


# Envía una consulta UPDATE a la DB con el id del item facilitado y realiza una
# actualización general de los datos.
def update_item(id, nombre, autor, editorial, año, categoria, estado):
    conn = sqlite3.connect("biblioteca")
    c = conn.cursor()

    c.execute(
        f"""
            UPDATE libros 
            SET nombre = "{nombre}", autor = "{autor}", 
            editorial = "{editorial}", año = "{año}", 
            categoria = "{categoria}", estado = "{estado}" WHERE id = {id}
        """
    )
    conn.commit()


# Envía una consulta SELECT a la DB y retorna el resultado en formato Dataframe.
# La cláusula WHERE (argumento 'x') puede ser suministrada por el usuario según
# su elección.
def myquery(x=""):
    conn = sqlite3.connect("biblioteca")
    c = conn.cursor()

    c.execute(
        f"""
            SELECT * FROM libros {x}
        """
    )
    conn.commit()

    query = pd.DataFrame(
        c.fetchall(),
        columns=["id", "nombre", "autor", "editorial", "año", "categoria", "estado"],
    )

    return query


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::USER FUNCTIONS:::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Ejecuta una acción INSERT sobre la DB al oprimir el botón "Añadir".
def agregar_libro(nombre, autor, editorial, año, categoria, estado):
    global mensaje_error
    if __validate_data__():
        insert_item(
            nombre.get(),
            autor.get(),
            editorial.get(),
            año.get(),
            categoria.get(),
            estado.get(),
        )
        showinfo(title="Aviso", message="Su libro fue cargado correctamente")
        __clearnbuild__()
        __clear_data_entry__()
    else:
        showerror(
            title="Error de campos inválidos",
            message="Controle que todos los campos contengan datos válidos"
            + mensaje_error,
        )


# Ejecuta una acción DELETE sobre la DB al oprimir el botón "Eliminar".
def eliminar_libro(id):
    global mensaje_error
    patron_id = re.compile("\d+")
    if re.fullmatch(patron_id, id.get()) != None:
        answer = askyesno(
            title="Confirmación",
            message="¿Realmente desea eliminar este libro?",
        )
        if answer:
            delete_item(id.get())
            showinfo(title="Aviso", message="Su libro fue eliminado correctamente")
            __clearnbuild__()
            __clear_data_entry__()
    else:
        showerror(
            title="Error de ID",
            message="El ID ingresado no es válido para ejecutar la acción"
            + mensaje_error,
        )


# Ejecuta una acción UPDATE sobre la DB al oprimir el botón "Modificarr".
def modificar_libro(id, nombre, autor, editorial, año, categoria, estado):
    global mensaje_error
    if __validate_data__():
        answer = askyesno(
            title="Confirmación",
            message="¿Realmente desea modificar este libro?",
        )
        if answer:
            update_item(
                id.get(),
                nombre.get(),
                autor.get(),
                editorial.get(),
                año.get(),
                categoria.get(),
                estado.get(),
            )
            showinfo(title="Aviso", message="Su libro fue modificado correctamente")
            __clearnbuild__()
            __clear_data_entry__()
    else:
        showerror(
            title="Error de campos inválidos",
            message="Controle que todos los campos contengan datos válidos"
            + mensaje_error,
        )


# Ejecuta una acción SELECT sobre la DB al oprimir el botón "Consultar".
def consultar(consulta):
    if __query_validation__(consulta.get()) != None:
        query = __query_validation__(consulta.get())
        __clear__
        __built__(query)


# Autocompleta los campos del Data Entry con los datos del libro# seleccionado
# por el usuario en el TreeView.
def select_item(a):
    item_ = tree.focus()
    selected = myquery(
        x="WHERE id = " + str(tree.item(item_)["values"][0])
    ).values.tolist()
    __clear_data_entry__()
    control_id.set(selected[0][0])
    control_nombre.set(selected[0][1])
    control_autor.set(selected[0][2])
    control_editorial.set(selected[0][3])
    control_año.set(selected[0][4])
    control_categoria.set(selected[0][5])
    control_estado.set(selected[0][6])


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::HIDDEN FUNCTIONS:::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# La función centra la ventana principal a partir de los datos de resolución de pantalla.
def __center_window__(win, window_width, window_height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    return f"{window_width}x{window_height}+{center_x}+{center_y}"


def __clearnbuild__():
    __clear__()
    __built__()


# Vacía el Treeview
def __clear__():
    for row in tree.get_children():
        tree.delete(row)


# Construye el TreeView con los datos retornados de una consulta SELECT a DB.
def __built__(x=""):
    __clear__()
    data = myquery(x).values.tolist()
    for i in range(0, len(data)):
        tree.insert(
            "",
            "0",
            values=(
                data[i][0],
                data[i][1],
                data[i][2],
                data[i][3],
                data[i][5],
                data[i][6],
            ),
        )


# Vacía todos los datos existentes en los campos de Data Entry.
def __clear_data_entry__():
    control_id.set("")
    control_nombre.set("")
    control_autor.set("")
    control_editorial.set("")
    control_año.set("")
    control_categoria.set("")
    control_estado.set("")


# Comprueba la validez de la expresión del campo solicitado en la búsqueda del usuario
# y retorna una consulta SQL en forma de STR o un mensaje de error en caso contrario.
def __query_validation__(y):
    global mensaje_error
    patron_id = re.compile("\d+")
    patron_nombre = re.compile("[a-z0-9\sáéíóúñ]+", flags=re.I)
    patron_autor = re.compile("[a-záéíóúñ\s]+", flags=re.I)
    patron_editorial = re.compile("[a-z0-9\sáéíóúñ]+", flags=re.I)
    patron_año = re.compile("(19[0-9]{2}|20[0-2][0-9])")
    patron_categoria = re.compile("(Ficción|Ensayo|Poesía|Filosofía|Sociología|Otros)")
    patron_estado = re.compile("(En Biblioteca|Prestado)")

    match y:
        case "Ver todo":
            __clear_data_entry__()
            return ""
        case "Buscar id":
            if re.fullmatch(patron_id, control_id.get()) == None:
                showerror(
                    title="Error de escritura",
                    message="Por favor, ingrese un ID válido para realizar la búsqueda."
                    + mensaje_error,
                )
            else:
                return f"WHERE id = {control_id.get()}"
        case "Buscar nombre":
            if re.fullmatch(patron_nombre, control_nombre.get()) == None:
                showerror(
                    title="Error de escritura",
                    message="Por favor, ingrese un nombre válido para realizar la búsqueda."
                    + mensaje_error,
                )
            else:
                return f"WHERE nombre LIKE '%{control_nombre.get()}%'"
        case "Buscar autor":
            if re.fullmatch(patron_autor, control_autor.get()) == None:
                showerror(
                    title="Error de escritura",
                    message="Por favor, ingrese un autor válido para realizar la búsqueda."
                    + mensaje_error,
                )
            else:
                return f"WHERE autor LIKE '%{control_autor.get()}%'"
        case "Buscar editorial":
            if re.fullmatch(patron_editorial, control_editorial.get()) == None:
                showerror(
                    title="Error de escritura",
                    message="Por favor, ingrese una editorial válida para realizar la búsqueda."
                    + mensaje_error,
                )
            else:
                return f"WHERE editorial LIKE '%{control_editorial.get()}%'"
        case "Buscar año":
            if re.fullmatch(patron_año, control_año.get()) == None:
                showerror(
                    title="Error de escritura",
                    message="Por favor, ingrese un año válido para realizar la búsqueda."
                    + mensaje_error,
                )
            else:
                return f"WHERE año = {control_año.get()}"
        case "Buscar categoria":
            if re.fullmatch(patron_categoria, control_categoria.get()) == None:
                showerror(
                    title="Error de escritura",
                    message="Por favor, ingrese una categoria válida para realizar la búsqueda."
                    + mensaje_error,
                )
            else:
                return f"WHERE categoria LIKE '%{control_categoria.get()}%'"
        case "Buscar estado":
            if re.fullmatch(patron_estado, control_estado.get()) == None:
                showerror(
                    title="Error de escritura",
                    message="Por favor, ingrese un estado válido para realizar la búsqueda."
                    + mensaje_error,
                )
            else:
                return f"WHERE estado = '{control_estado.get()}'"


# Comprueba la validez de las expresiones en todos los campos del data entry y retorna
# True si son todas correctas o False en caso contrario.
def __validate_data__():
    patron_id = re.compile("\d*")
    patron_nombre = re.compile("[a-z0-9\sáéíóúñ]+", flags=re.I)
    patron_autor = re.compile("[a-záéíñóú\s]+", flags=re.I)
    patron_editorial = re.compile("[a-z0-9\sáéñíóú]+", flags=re.I)
    patron_año = re.compile("(19|20)[0-9]{2}")
    patron_categoria = re.compile("(Ficción|Ensayo|Poesía|Filosofía|Sociología|Otros)")
    patron_estado = re.compile("(En Biblioteca|Prestado)")

    con0 = False
    con1 = False
    con2 = False
    con3 = False
    con4 = False
    con5 = False
    con6 = False

    if re.fullmatch(patron_nombre, control_nombre.get()) != None:
        con0 = True
    if re.fullmatch(patron_autor, control_autor.get()) != None:
        con1 = True
    if re.fullmatch(patron_editorial, control_editorial.get()) != None:
        con2 = True
    if re.fullmatch(patron_año, control_año.get()) != None:
        con3 = True
    if re.fullmatch(patron_categoria, control_categoria.get()) != None:
        con4 = True
    if re.fullmatch(patron_estado, control_estado.get()) != None:
        con5 = True
    if re.fullmatch(patron_id, control_id.get()) != None:
        con6 = True

    if con0 & con1 & con2 & con3 & con4 & con5 & con6:
        return True
    else:
        return False


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::TKINTER´S INTERFACE::::::::::::::::::::::::::::::::::::::
#:::::::::::::::Seteo general de la ventana. Creación y posicionamiento de widgets::::::::::::


create_db()
ventana = tk.Tk()
ventana.title("Hermes BookSearch 1.0")
ventana.config(bg="#091430")
ventana.geometry(__center_window__(ventana, 700, 750))

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

#::::::::::::::::::::::::::::::::::::::CONTROL VARIABLES::::::::::::::::::::::::::::::::::::::
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

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::LABELS::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::Etiquetas de los campos de Data Entry:::::::::::::::::::::::::::

fuente = Font(family="Consolas", size=12, weight="bold")
s = ttk.Style(ventana)
s.configure("TLabel", background="#091430", foreground="white")

lb_id = ttk.Label(ventana, text="ID", anchor=tk.E, style="TLabel", font=fuente)
lb_nombre = ttk.Label(ventana, text="Nombre", anchor=tk.E, style="TLabel", font=fuente)
lb_autor = ttk.Label(ventana, text="Autor", anchor=tk.E, style="TLabel", font=fuente)
lb_editorial = ttk.Label(
    ventana, text="Editorial", anchor=tk.E, style="TLabel", font=fuente
)
lb_año = ttk.Label(
    ventana, text="Año publicación", anchor=tk.E, style="TLabel", font=fuente
)
lb_categoria = ttk.Label(
    ventana, text="Categoría", anchor=tk.E, style="TLabel", font=fuente
)
lb_estado = ttk.Label(ventana, text="Estado", anchor=tk.E, style="TLabel", font=fuente)

lb_id.place(x=82, y=28, width=103, height=30)
lb_nombre.place(x=82, y=73, width=103, height=30)
lb_autor.place(x=82, y=118, width=103, height=30)
lb_editorial.place(x=82, y=163, width=103, height=30)
lb_año.place(x=18, y=208, width=167, height=30)
lb_categoria.place(x=92, y=253, width=93, height=30)
lb_estado.place(x=92, y=298, width=93, height=30)

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::::::::::::::::::ENTRIES & COMBOBOXES::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::Entries y Comboboxes de los campos de Data Entry:::::::::::::::::::::::

box_id = tk.Entry(ventana, textvariable=control_id, bg="#A5FFCE", font=("Consolas 11"))
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

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::BUTTONS::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::Botonera general para interacción con el usuario:::::::::::::::::::::::::


bt_agregar = tk.Button(
    ventana,
    text="Añadir",
    background="#02FF3A",
    activebackground="#751C3C",
    font=("Consolas 12 bold"),
    command=lambda: agregar_libro(
        control_nombre,
        control_autor,
        control_editorial,
        control_año,
        control_categoria,
        control_estado,
    ),
)
bt_eliminar = tk.Button(
    ventana,
    text="Eliminar",
    background="#02FF3A",
    activebackground="#751C3C",
    font=("Consolas 12 bold"),
    command=lambda: eliminar_libro(control_id),
)
bt_modificar = tk.Button(
    ventana,
    text="Modificar",
    background="#02FF3A",
    activebackground="#751C3C",
    font=("Consolas 12 bold"),
    command=lambda: modificar_libro(
        control_id,
        control_nombre,
        control_autor,
        control_editorial,
        control_año,
        control_categoria,
        control_estado,
    ),
)
bt_consultar = tk.Button(
    ventana,
    text="Consultar",
    background="#02FF3A",
    activebackground="#751C3C",
    font=("Consolas 12 bold"),
    command=lambda: consultar(control_consulta),
)

bt_agregar.place(x=25, y=370, width=136, height=36)
bt_eliminar.place(x=196, y=370, width=136, height=36)
bt_modificar.place(x=367, y=370, width=136, height=36)
bt_consultar.place(x=538, y=370, width=136, height=36)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::TREEVIEW:::::::::::::::::::::::::::::::::::::::::::::::
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
tree.bind("<ButtonRelease-1>", select_item)

__built__()


ventana.mainloop()
