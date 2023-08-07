import sys

sys.path.append("../library")
import re
import tkinter as tk
from modelos.estructura_base import Libro
from modelos.cuadros_de_dialogo import Mensajes


class DataOps(Mensajes):
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
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar id"
                    clausula = control_id.get()
                    return sobre, clausula
            case "Buscar nombre":
                if re.fullmatch(patron_nombre, control_nombre.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar nombre"
                    clausula = control_nombre.get()
                    return sobre, clausula
            case "Buscar autor":
                if re.fullmatch(patron_autor, control_autor.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar autor"
                    clausula = control_autor.get()
                    return sobre, clausula
            case "Buscar editorial":
                if re.fullmatch(patron_editorial, control_editorial.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar editorial"
                    clausula = control_editorial.get()
                    return sobre, clausula
            case "Buscar año":
                if re.fullmatch(patron_año, control_año.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar año"
                    clausula = control_año.get()
                    return sobre, clausula
            case "Buscar categoria":
                if re.fullmatch(patron_categoria, control_categoria.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar categoria"
                    clausula = control_categoria.get()
                    return sobre, clausula
            case "Buscar estado":
                if re.fullmatch(patron_estado, control_estado.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
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
