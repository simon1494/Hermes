import pandas as pd
import sqlite3
import re
from tkinter.messagebox import *
from peewee import *

db = SqliteDatabase("biblioteca.db")


class BaseModel(Model):
    class Meta:
        database = db


class Libro(BaseModel):
    id = PrimaryKeyField()
    nombre = TextField()
    autor = TextField()
    editorial = TextField()
    año = TimeField()
    categoria = TextField()
    estado = TextField()

    class Meta:
        table_name = "libros"


class Database:
    # Comprueba si existe una base de datos y, en caso de no existir, la crea.

    def create_db(self):
        conn = sqlite3.connect("biblioteca.db")
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
    def insert_item(self, nombre, autor, editorial, año, categoria, estado):
        libro = Libro()
        libro.nombre = nombre
        libro.autor = autor
        libro.editorial = editorial
        libro.año = año
        libro.categoria = categoria
        libro.estado = estado
        libro.save()

    # Envía una consulta DELETE a la DB con el id del item facilitado por el usuario.
    def delete_item(self, id):
        registro = Libro.get(Libro.id == id)
        registro.delete_instance()

    # Envía una consulta UPDATE a la DB con el id del item facilitado y realiza una
    # actualización general de los datos.

    def update_item(self, id, nombre, autor, editorial, año, categoria, estado):
        registro = Libro.update(
            nombre=nombre,
            autor=autor,
            editorial=editorial,
            año=año,
            categoria=categoria,
            estado=estado,
        ).where(Libro.id == id)
        registro.execute()

    # Envía una consulta SELECT a la DB y retorna el resultado en formato Dataframe.
    # La cláusula WHERE (argumento 'x') puede ser suministrada por el usuario según
    # su elección.

    def myquery(self, x=""):
        conn = sqlite3.connect("biblioteca.db")
        c = conn.cursor()

        c.execute(
            f"""
                SELECT * FROM libros {x}
            """
        )
        conn.commit()

        query = pd.DataFrame(
            c.fetchall(),
            columns=[
                "id",
                "nombre",
                "autor",
                "editorial",
                "año",
                "categoria",
                "estado",
            ],
        )

        return query


class Apoyo(Database):
    # Ejecuta una acción INSERT sobre la DB al oprimir el botón "Añadir".
    def agregar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        if self.__validate_data(id, nombre, autor, editorial, año, categoria, estado):
            self.insert_item(
                nombre.get(),
                autor.get(),
                editorial.get(),
                año.get(),
                categoria.get(),
                estado.get(),
            )
            showinfo(title="Aviso", message="Su libro fue cargado correctamente")
            self.__clearnbuild(tree)
            self.__clear_data_entry(
                id, nombre, autor, editorial, año, categoria, estado
            )
        else:
            showerror(
                title="Error de campos inválidos",
                message="Controle que todos los campos contengan datos válidos"
                + mensaje_error,
            )

    # Ejecuta una acción DELETE sobre la DB al oprimir el botón "Eliminar".
    def eliminar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        patron_id = re.compile("\d+")
        if re.fullmatch(patron_id, id.get()) != None:
            answer = askyesno(
                title="Confirmación",
                message="¿Realmente desea eliminar este libro?",
            )
            if answer:
                self.delete_item(id.get())
                showinfo(title="Aviso", message="Su libro fue eliminado correctamente")
                self.__clearnbuild(tree)
                self.__clear_data_entry(
                    id, nombre, autor, editorial, año, categoria, estado
                )
        else:
            showerror(
                title="Error de ID",
                message="El ID ingresado no es válido para ejecutar la acción"
                + mensaje_error,
            )

    # Ejecuta una acción UPDATE sobre la DB al oprimir el botón "Modificarr".
    def modificar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        if self.__validate_data(id, nombre, autor, editorial, año, categoria, estado):
            answer = askyesno(
                title="Confirmación",
                message="¿Realmente desea modificar este libro?",
            )
            if answer:
                self.update_item(
                    id.get(),
                    nombre.get(),
                    autor.get(),
                    editorial.get(),
                    año.get(),
                    categoria.get(),
                    estado.get(),
                )
                showinfo(title="Aviso", message="Su libro fue modificado correctamente")
                self.__clearnbuild(tree)
                self.__clear_data_entry(
                    id, nombre, autor, editorial, año, categoria, estado
                )
        else:
            showerror(
                title="Error de campos inválidos",
                message="Controle que todos los campos contengan datos válidos"
                + mensaje_error,
            )

    # Ejecuta una acción SELECT sobre la DB al oprimir el botón "Consultar".
    def consultar(
        self,
        consulta,
        id,
        nombre,
        autor,
        editorial,
        año,
        categoria,
        estado,
        mensaje_error,
        tree,
    ):
        if (
            self.__query_validation(
                consulta.get(),
                id,
                nombre,
                autor,
                editorial,
                año,
                categoria,
                estado,
                mensaje_error,
                tree,
            )
            != None
        ):
            query = self.__query_validation(
                consulta.get(),
                id,
                nombre,
                autor,
                editorial,
                año,
                categoria,
                estado,
                mensaje_error,
                tree,
            )
            self.__clear(tree)
            self._built(tree, x=query)

    # Autocompleta los campos del Data Entry con los datos del libro# seleccionado
    # por el usuario en el TreeView.
    def select_item(
        self,
        a,
        b,
        c,
        d,
        e,
        f,
        g,
        h,
    ):
        item_ = a.focus()
        selected = self.myquery(
            x="WHERE id = " + str(a.item(item_)["values"][0])
        ).values.tolist()
        self.__clear_data_entry(b, c, d, e, f, g, h)
        b.set(selected[0][0])
        c.set(selected[0][1])
        d.set(selected[0][2])
        e.set(selected[0][3])
        f.set(selected[0][4])
        g.set(selected[0][5])
        h.set(selected[0][6])

    # La función centra la ventana principal a partir de los datos de resolución de pantalla.
    @staticmethod
    def center_window(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y}"

    def __clearnbuild(self, tree):
        self.__clear(tree)
        self._built(tree)

    # Vacía el Treeview
    def __clear(self, tree):
        for row in tree.get_children():
            tree.delete(row)

    # Construye el TreeView con los datos retornados de una consulta SELECT a DB.
    def _built(self, tree, x=""):
        self.__clear(tree)
        data = self.myquery(x).values.tolist()
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
    def __clear_data_entry(
        self,
        control_id,
        control_nombre,
        control_autor,
        control_editorial,
        control_año,
        control_categoria,
        control_estado,
    ):
        control_id.set("")
        control_nombre.set("")
        control_autor.set("")
        control_editorial.set("")
        control_año.set("")
        control_categoria.set("")
        control_estado.set("")

    # Comprueba la validez de la expresión del campo solicitado en la búsqueda del usuario
    # y retorna una consulta SQL en forma de STR o un mensaje de error en caso contrario.
    def __query_validation(
        self,
        y,
        control_id,
        control_nombre,
        control_autor,
        control_editorial,
        control_año,
        control_categoria,
        control_estado,
        mensaje_error,
        tree,
    ):
        patron_id = re.compile("\d+")
        patron_nombre = re.compile("[a-z0-9\sáéíóúñ]+", flags=re.I)
        patron_autor = re.compile("[a-záéíóúñ\s]+", flags=re.I)
        patron_editorial = re.compile("[a-z0-9\sáéíóúñ]+", flags=re.I)
        patron_año = re.compile("(19[0-9]{2}|20[0-2][0-9])")
        patron_categoria = re.compile(
            "(Ficción|Ensayo|Poesía|Filosofía|Sociología|Otros)"
        )
        patron_estado = re.compile("(En Biblioteca|Prestado)")

        match y:
            case "Ver todo":
                self.__clear_data_entry(
                    control_id,
                    control_nombre,
                    control_autor,
                    control_editorial,
                    control_año,
                    control_categoria,
                    control_estado,
                )
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
    def __validate_data(
        self,
        control_id,
        control_nombre,
        control_autor,
        control_editorial,
        control_año,
        control_categoria,
        control_estado,
    ):
        patron_id = re.compile("\d*")
        patron_nombre = re.compile("[a-z0-9\sáéíóúñ]+", flags=re.I)
        patron_autor = re.compile("[a-záéíñóú\s]+", flags=re.I)
        patron_editorial = re.compile("[a-z0-9\sáéñíóú]+", flags=re.I)
        patron_año = re.compile("(19|20)[0-9]{2}")
        patron_categoria = re.compile(
            "(Ficción|Ensayo|Poesía|Filosofía|Sociología|Otros)"
        )
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
