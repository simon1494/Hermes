import pandas as pd
import re
from tkinter.messagebox import *
import peewee as pw

db = pw.SqliteDatabase("biblioteca.db")


class ModeloBase(pw.Model):
    class Meta:
        database = db


class Libro(ModeloBase):
    id = pw.PrimaryKeyField()
    nombre = pw.TextField()
    autor = pw.TextField()
    editorial = pw.TextField()
    año = pw.TimeField()
    categoria = pw.TextField()
    estado = pw.TextField()

    class Meta:
        table_name = "libros"


class Database:
    # Comprueba si existe una base de datos y, en caso de no existir, la crea.
    @staticmethod
    def crear_db():
        db.connect()
        db.create_tables([Libro])

    # Envía una consulta INSERT a la DB con los datos ingresados por el usuario.
    @staticmethod
    def alta_db(nombre, autor, editorial, año, categoria, estado):
        libro = Libro()
        libro.nombre = nombre
        libro.autor = autor
        libro.editorial = editorial
        libro.año = año
        libro.categoria = categoria
        libro.estado = estado
        libro.save()

    # Envía una consulta DELETE a la DB con el id del item facilitado por el usuario.
    @staticmethod
    def baja_db(id):
        registro = Libro.get(Libro.id == id)
        registro.delete_instance()

    # Envía una consulta UPDATE a la DB con el id del item facilitado y realiza una
    # actualización general de los datos.
    @staticmethod
    def modificar_db(id, nombre, autor, editorial, año, categoria, estado):
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

    def consultar_db(self, sobre=None, clausula=None, df=True):
        match sobre:
            case "Ver todo":
                resultado = Libro.select().where(Libro.id > 0)
            case None:
                resultado = Libro.select().where(Libro.id > 0)
            case "Buscar id":
                resultado = Libro.select().where(Libro.id == clausula)
            case "Buscar nombre":
                resultado = Libro.select().where(Libro.nombre == clausula)
            case "Buscar autor":
                resultado = Libro.select().where(Libro.autor == clausula)
            case "Buscar editorial":
                resultado = Libro.select().where(Libro.editorial > clausula)
            case "Buscar año":
                resultado = Libro.select().where(Libro.año == clausula)
            case "Buscar categoria":
                resultado = Libro.select().where(Libro.categoria == clausula)
            case "Buscar estado":
                resultado = Libro.select().where(Libro.estado == clausula)

        # Crear el DataFrame a partir de la lista de datos de las filas
        final = self._convertir_query(resultado, df)

        return final

    @staticmethod
    def _convertir_query(resultado, df):
        final = []
        for registro in resultado:
            final.append(
                [
                    registro.id,
                    registro.nombre,
                    registro.autor,
                    registro.editorial,
                    registro.año,
                    registro.categoria,
                    registro.estado,
                ]
            )

        if df:
            final = pd.DataFrame(
                final,
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
        return final


class LogicaInterna:

    # Autocompleta los campos del Data Entry con los datos del libro# seleccionado
    # por el usuario en el TreeView.
    def seleccionar_item(
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
        try:
            item_ = a.focus()
            selected = self._convertir_query(
                Libro.select().where(Libro.id == a.item(item_)["values"][0]), False
            )
            self.blanquear_entradas(b, c, d, e, f, g, h)
            b.set(selected[0][0])
            c.set(selected[0][1])
            d.set(selected[0][2])
            e.set(selected[0][3])
            f.set(selected[0][4])
            g.set(selected[0][5])
            h.set(selected[0][6])
        except IndexError:
            pass  # Pasa por alto el error en consola que ocurre al clickear en un espacio no valido del Treeview

    # La función centra la ventana principal a partir de los datos de resolución de pantalla.
    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y}"

    def limpiar_y_armar(self, tree):
        self.limpiar_treeview(tree)
        self.armar_treeview(tree)

    # Vacía el Treeview
    def limpiar_treeview(self, tree):
        for row in tree.get_children():
            tree.delete(row)

    # Construye el TreeView con los datos retornados de una consulta SELECT a DB.
    def armar_treeview(self, tree, sobre=None, clausula=None):
        self.limpiar_treeview(tree)
        data = self.consultar_db(sobre, clausula, df=False)
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
    def blanquear_entradas(
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
    def armar_consulta(
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
                self.blanquear_entradas(
                    control_id,
                    control_nombre,
                    control_autor,
                    control_editorial,
                    control_año,
                    control_categoria,
                    control_estado,
                )
                sobre = "Ver todo"
                clausula = None
                return sobre, clausula
            case "Buscar id":
                if re.fullmatch(patron_id, control_id.get()) == None:
                    showerror(
                        title="Error de escritura",
                        message="Por favor, ingrese un ID válido para realizar la búsqueda."
                        + mensaje_error,
                    )
                else:
                    sobre = "Buscar id"
                    clausula = control_id.get()
                    return sobre, clausula
            case "Buscar nombre":
                if re.fullmatch(patron_nombre, control_nombre.get()) == None:
                    showerror(
                        title="Error de escritura",
                        message="Por favor, ingrese un nombre válido para realizar la búsqueda."
                        + mensaje_error,
                    )
                else:
                    sobre = "Buscar nombre"
                    clausula = control_nombre.get()
                    return sobre, clausula
            case "Buscar autor":
                if re.fullmatch(patron_autor, control_autor.get()) == None:
                    showerror(
                        title="Error de escritura",
                        message="Por favor, ingrese un autor válido para realizar la búsqueda."
                        + mensaje_error,
                    )
                else:
                    sobre = "Buscar autor"
                    clausula = control_autor.get()
                    return sobre, clausula
            case "Buscar editorial":
                if re.fullmatch(patron_editorial, control_editorial.get()) == None:
                    showerror(
                        title="Error de escritura",
                        message="Por favor, ingrese una editorial válida para realizar la búsqueda."
                        + mensaje_error,
                    )
                else:
                    sobre = "Buscar editorial"
                    clausula = control_editorial.get()
                    return sobre, clausula
            case "Buscar año":
                if re.fullmatch(patron_año, control_año.get()) == None:
                    showerror(
                        title="Error de escritura",
                        message="Por favor, ingrese un año válido para realizar la búsqueda."
                        + mensaje_error,
                    )
                else:
                    sobre = "Buscar año"
                    clausula = control_año.get()
                    return sobre, clausula
            case "Buscar categoria":
                if re.fullmatch(patron_categoria, control_categoria.get()) == None:
                    showerror(
                        title="Error de escritura",
                        message="Por favor, ingrese una categoria válida para realizar la búsqueda."
                        + mensaje_error,
                    )
                else:
                    sobre = "Buscar categoria"
                    clausula = control_categoria.get()
                    return sobre, clausula
            case "Buscar estado":
                if re.fullmatch(patron_estado, control_estado.get()) == None:
                    showerror(
                        title="Error de escritura",
                        message="Por favor, ingrese un estado válido para realizar la búsqueda."
                        + mensaje_error,
                    )
                else:
                    sobre = "Buscar estado"
                    clausula = control_estado.get()
                    return sobre, clausula

    # Comprueba la validez de las expresiones en todos los campos del data entry y retorna
    # True si son todas correctas o False en caso contrario.
    def validar_entradas(
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


class Api(Database, LogicaInterna):
    # Ejecuta una acción INSERT sobre la DB al oprimir el botón "Añadir".
    def agregar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        if self.validar_entradas(id, nombre, autor, editorial, año, categoria, estado):
            self.alta_db(
                nombre.get(),
                autor.get(),
                editorial.get(),
                año.get(),
                categoria.get(),
                estado.get(),
            )
            showinfo(title="Aviso", message="Su libro fue cargado correctamente")
            self.limpiar_y_armar(tree)
            self.blanquear_entradas(
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
                self.baja_db(id.get())
                showinfo(title="Aviso", message="Su libro fue eliminado correctamente")
                self.limpiar_y_armar(tree)
                self.blanquear_entradas(
                    id, nombre, autor, editorial, año, categoria, estado
                )
        else:
            showerror(
                title="Error de ID",
                message="El ID ingresado no es válido para ejecutar la acción"
                + mensaje_error,
            )

    # Ejecuta una acción UPDATE sobre la DB al oprimir el botón "Modificar".
    def modificar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        if self.validar_entradas(id, nombre, autor, editorial, año, categoria, estado):
            answer = askyesno(
                title="Confirmación",
                message="¿Realmente desea modificar este libro?",
            )
            if answer:
                self.modificar_db(
                    id.get(),
                    nombre.get(),
                    autor.get(),
                    editorial.get(),
                    año.get(),
                    categoria.get(),
                    estado.get(),
                )
                showinfo(title="Aviso", message="Su libro fue modificado correctamente")
                self.limpiar_y_armar(tree)
                self.blanquear_entradas(
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
            self.armar_consulta(
                consulta.get(),
                id,
                nombre,
                autor,
                editorial,
                año,
                categoria,
                estado,
                mensaje_error,
            )
            != None
        ):
            sobre, clausula = self.armar_consulta(
                consulta.get(),
                id,
                nombre,
                autor,
                editorial,
                año,
                categoria,
                estado,
                mensaje_error,
            )
            self.limpiar_treeview(tree)
            self.armar_treeview(tree, sobre, clausula)
