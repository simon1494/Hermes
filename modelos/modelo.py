import sys

sys.path.append("../library")
import pandas as pd
import re
import peewee as pw
from screeninfo import get_monitors
from tkinter.messagebox import *

"""
modelo.py:
    Contiene las clases encargadas de administrar la conexión con la base de datos, la lógica interna del nuestra aplicación y funciones de validación de datos.
"""

db = pw.SqliteDatabase("biblioteca.db")


class ModeloBase(pw.Model):
    """
    Clase que defina la base de datos para el ORM.
    """

    class Meta:
        """.. sphinx-autodoc-skip::"""

        database = db


class Libro(ModeloBase):
    """
    Clase que define la tabla donde cargaremos los registros en la base de datos para el ORM
    """

    id = pw.PrimaryKeyField()
    nombre = pw.TextField()
    autor = pw.TextField()
    editorial = pw.TextField()
    año = pw.TimeField()
    categoria = pw.TextField()
    estado = pw.TextField()

    class Meta:
        """.. sphinx-autodoc-skip::"""

        table_name = "libros"


class Database:
    @staticmethod
    def crear_db():
        """
        Crea una base de datos donde se almacenará la información de nuestra aplicación. La función se ejecuta cada vez que la aplicación es abierta, pero en el caso de que ya exista una base creada, entonces no tendrá ningún efecto.
        """
        db.connect()
        db.create_tables([Libro])

    @staticmethod
    def alta_db(nombre, autor, editorial, año, categoria, estado):
        """
        Genera el alta de un registro en la base de datos de nuestra aplicación.

        :param nombre: String. Nombre del libro.
        :param autor: String. Nombre del autor del libro.
        :param editorial: String. Nombre de la editorial del libro.
        :param año: String. Año de publicación del libro.
        :param categoria: String. Categoría a la que pertenece el libro.
        :param estado: String. Estado de existencia del libro en la biblioteca.
        """
        libro = Libro()
        libro.nombre = nombre
        libro.autor = autor
        libro.editorial = editorial
        libro.año = año
        libro.categoria = categoria
        libro.estado = estado
        libro.save()

    @staticmethod
    def baja_db(id):
        """
        Genera la baja de un registro en la base de datos de nuestra aplicación.

        :param id: Integer. ID del libro que se desea eliminar."""
        registro = Libro.get(Libro.id == id)
        registro.delete_instance()

    @staticmethod
    def modificar_db(id, nombre, autor, editorial, año, categoria, estado):
        """
        Actualiza los campos de un registro existente en la base de datos de nuestra aplicación.

        :param id: Integer. ID del libro que se desea actualizar.
        :param nombre: String. Nombre del libro.
        :param autor: String. Nombre del autor del libro.
        :param editorial: String. Nombre de la editorial del libro.
        :param año: String. Año de publicación del libro.
        :param categoria: String. Categoría a la que pertenece el libro.
        :param estado: String. Estado de existencia del libro en la biblioteca.
        """
        registro = Libro.update(
            nombre=nombre,
            autor=autor,
            editorial=editorial,
            año=año,
            categoria=categoria,
            estado=estado,
        ).where(Libro.id == id)
        registro.execute()

    def consultar_db(self, sobre=None, clausula=None, df=True):
        """
        Actualiza el Treeview de nuestra aplicación con el resultado consulta sobre el campo que elijamos.

        :param sobre: String. Determina sobre qué campo de nuestra base se ejecutará la consulta. Por default None, lo que establece una busqueda de todos los registros.
        :param clausula: String. Determina la expresión a matchear en los registros del campo seleccionado. Por default None, lo que establece una busqueda sin criterio.
        :param df: Booleano. Determina si el resultado de la consulta en base de regresa en formado dataframe o lista. Por default en True (devuelve dataframe)
        :return: Datos de consulta en formato d   ataframe o lista"""
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
        """
        Convierte el resultado de una consulta a base en dataframe o lista según corresponda.

        :param resultado: Objeto propio del ORM Peewee. Es el resultado de una consulta.
        :param df: Booleano. Seteado en True convierte el resultado en dataframe; de lo contrario, lista.
        :return: Dataframe o lista. Resultado de la consulta a base convertido en formato conveniente.
        """
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
    def seleccionar_item(
        self,
        tree,
        id,
        nombre,
        autor,
        editorial,
        año,
        categoria,
        estado,
    ):
        """
        Ejecuta un autocompletado de los campos del data entry al clickear sobre un item del treeview.

        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :param mensaje_error: String. Mensaje de error a mostrar en caso de consulta inválida.
        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        """
        try:
            item_ = tree.focus()
            selected = self._convertir_query(
                Libro.select().where(Libro.id == tree.item(item_)["values"][0]), False
            )
            self.blanquear_entradas(
                id, nombre, autor, editorial, año, categoria, estado
            )
            id.set(selected[0][0])
            nombre.set(selected[0][1])
            autor.set(selected[0][2])
            editorial.set(selected[0][3])
            año.set(selected[0][4])
            categoria.set(selected[0][5])
            estado.set(selected[0][6])
        except IndexError:
            pass  # Pasa por alto el error en consola que ocurre al clickear en un espacio no valido del Treeview

    def limpiar_y_armar(self, tree):
        """
        Blanquea y rearma el Treeview de nuestra aplicación.

        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        """
        self.limpiar_treeview(tree)
        self.armar_treeview(tree)

    def limpiar_treeview(self, tree):
        """
        Blanquea el Treeview de nuestra aplicación.

        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        """
        for row in tree.get_children():
            tree.delete(row)

    def armar_treeview(self, tree, sobre=None, clausula=None):
        """
        Construye el Treeview de nuestra aplicación a partir de una consulta realizada a la base de datos.

        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        :param sobre: String. Argumento interno para ejecutar la consulta. Define sobre qué campo se ejecutará. Por default en None, lo cual determina una consulta general.
        :param clausula: String. Argumento interno para ejecutar la consulta. Define cual será el criterio de búsqueda. Por default en None, lo cual determina una consulta sin criterio.
        """
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
        """
        Realiza un blanqueo de todos los data entry de nuestra aplicación.

        :param control_id: Stringvar. Variable de control con datos del ID del libro.
        :param control_nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param control_autor: Stringvar. Variable de control con datos del autor del libro.
        :param control_editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param control_año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param control_categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param control_estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        """
        control_id.set("")
        control_nombre.set("")
        control_autor.set("")
        control_editorial.set("")
        control_año.set("")
        control_categoria.set("")
        control_estado.set("")

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
        """
        Comprueba la validez de la expresión del campo solicitado en la búsqueda del usuario y lo convierte a un formato adecuado para realizar una consulta por ORM. En vaso de consulta inválida, lanza mensaje de error.

        :param y: String. Representa una elección realizada por el usuario sobre qué tipo de consulta realizar.
        :param control_id: Stringvar. Variable de control con datos del ID del libro.
        :param control_nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param control_autor: Stringvar. Variable de control con datos del autor del libro.
        :param control_editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param control_año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param control_categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param control_estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :mensaje_error: String. Mensaje de error a mostrar en caso de consulta inválida.
        :return: Campo de la base (String) y clausula de la consulta a realizar (String).
        """
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
        """
        Comprueba la validez de las expresiones en todos los campos del data entry.

        :param control_id: Stringvar. Variable de control con datos del ID del libro.
        :param control_nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param control_autor: Stringvar. Variable de control con datos del autor del libro.
        :param control_editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param control_año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param control_categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param control_estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :return: True si la consulta es válida o False en caso contrario.
        """
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
    def agregar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        """
        Ejecuta instrucciones de alta al clickar el botón 'Añadir'. Luego, limpia y actualiza el treeview. En caso de datos inválidos, lanza mensaje de error.

        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :param mensaje_error: String. Mensaje de error a mostrar en caso de consulta inválida.
        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        """
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

    def eliminar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        """
        Ejecuta instrucciones de baja al clickar el botón 'Eliminar'. Luego, limpia y actualiza el treeview.

        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :param mensaje_error: String. Mensaje de error a mostrar en caso de consulta inválida.
        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        """
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

    def modificar_libro(
        self, id, nombre, autor, editorial, año, categoria, estado, mensaje_error, tree
    ):
        """
        Ejecuta instrucciones de actualización al clickar el botón 'Modificar'. Luego, limpia y actualiza el treeview. En caso de datos inválidos, lanza mensaje de error.

        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :param mensaje_error: String. Mensaje de error a mostrar en caso de consulta inválida.
        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        """
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
        """
        Ejecuta instrucciones de consulta al clickar el botón 'Consultar'. Luego, limpia y actualiza el treeview. En caso de datos inválidos, lanza mensaje de error.

        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :param mensaje_error: String. Mensaje de error a mostrar en caso de consulta inválida.
        :param tree: Objeto de clase Treeview. Representa el treeview de nuestra aplicación.
        """
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
