import sys

sys.path.append("../library")
import re
from clases.cuadros_de_dialogo import Mensajes


class WidgetOps(Mensajes):
    def seleccionar_item(self, tree, variables_de_control):
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

        id = variables_de_control["id"]
        nombre = variables_de_control["nombre"]
        autor = variables_de_control["autor"]
        editorial = variables_de_control["editorial"]
        año = variables_de_control["año"]
        categoria = variables_de_control["categoria"]
        estado = variables_de_control["estado"]

        try:
            item_ = tree.focus()
            item_2 = tree.item(item_)["values"][0]
            selected = self.objeto_observado.consultar(
                sobre="Buscar id", clausula=item_2, df=False
            )
            self.blanquear_entradas(variables_de_control)
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
        data = self.objeto_observado.consultar(sobre, clausula, df=False)
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

    def blanquear_entradas(self, variables_de_control):
        """
        Realiza un blanqueo de todos los data entry de nuestra aplicación.

        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        """
        id = variables_de_control["id"]
        nombre = variables_de_control["nombre"]
        autor = variables_de_control["autor"]
        editorial = variables_de_control["editorial"]
        año = variables_de_control["año"]
        categoria = variables_de_control["categoria"]
        estado = variables_de_control["estado"]

        id.set("")
        nombre.set("")
        autor.set("")
        editorial.set("")
        año.set("")
        categoria.set("")
        estado.set("")

    def armar_consulta(self, y, variables_de_control, mensaje_error):
        """
        Comprueba la validez de la expresión del campo solicitado en la búsqueda del usuario y lo convierte a un formato adecuado para realizar una consulta por ORM. En vaso de consulta inválida, lanza mensaje de error.

        :param y: String. Representa una elección realizada por el usuario sobre qué tipo de consulta realizar.
        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :mensaje_error: String. Mensaje de error a mostrar en caso de consulta inválida.
        :return: Campo de la base (String) y clausula de la consulta a realizar (String).
        """

        id = variables_de_control["id"]
        nombre = variables_de_control["nombre"]
        autor = variables_de_control["autor"]
        editorial = variables_de_control["editorial"]
        año = variables_de_control["año"]
        categoria = variables_de_control["categoria"]
        estado = variables_de_control["estado"]

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
                    id,
                    nombre,
                    autor,
                    editorial,
                    año,
                    categoria,
                    estado,
                )
                sobre = "Ver todo"
                clausula = None
                return sobre, clausula
            case "Buscar id":
                if re.fullmatch(patron_id, id.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar id"
                    clausula = id.get()
                    return sobre, clausula
            case "Buscar nombre":
                if re.fullmatch(patron_nombre, nombre.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar nombre"
                    clausula = nombre.get()
                    return sobre, clausula
            case "Buscar autor":
                if re.fullmatch(patron_autor, autor.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar autor"
                    clausula = autor.get()
                    return sobre, clausula
            case "Buscar editorial":
                if re.fullmatch(patron_editorial, editorial.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar editorial"
                    clausula = editorial.get()
                    return sobre, clausula
            case "Buscar año":
                if re.fullmatch(patron_año, año.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar año"
                    clausula = año.get()
                    return sobre, clausula
            case "Buscar categoria":
                if re.fullmatch(patron_categoria, categoria.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar categoria"
                    clausula = categoria.get()
                    return sobre, clausula
            case "Buscar estado":
                if re.fullmatch(patron_estado, estado.get()) == None:
                    self.mostrar_mensaje_error(f"{mensaje_error}")
                else:
                    sobre = "Buscar estado"
                    clausula = estado.get()
                    return sobre, clausula

    def validar_entradas(self, variables_de_control):
        """
        Comprueba la validez de las expresiones en todos los campos del data entry.

        :param id: Stringvar. Variable de control con datos del ID del libro.
        :param nombre: Stringvar. Variable de control con datos del nombre del libro.
        :param autor: Stringvar. Variable de control con datos del autor del libro.
        :param editorial: Stringvar. Variable de control con datos de la editorial del libro.
        :param año: Stringvar. Variable de control con datos del año de publicación del libro.
        :param categoria: Stringvar. Variable de control con datos de la categoría del libro.
        :param estado: Stringvar. Variable de control con datos del estado de existencia del libro.
        :return: True si la consulta es válida o False en caso contrario.
        """

        id = variables_de_control["id"]
        nombre = variables_de_control["nombre"]
        autor = variables_de_control["autor"]
        editorial = variables_de_control["editorial"]
        año = variables_de_control["año"]
        categoria = variables_de_control["categoria"]
        estado = variables_de_control["estado"]

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

        if re.fullmatch(patron_nombre, nombre.get()) != None:
            con0 = True
        if re.fullmatch(patron_autor, autor.get()) != None:
            con1 = True
        if re.fullmatch(patron_editorial, editorial.get()) != None:
            con2 = True
        if re.fullmatch(patron_año, año.get()) != None:
            con3 = True
        if re.fullmatch(patron_categoria, categoria.get()) != None:
            con4 = True
        if re.fullmatch(patron_estado, estado.get()) != None:
            con5 = True
        if re.fullmatch(patron_id, id.get()) != None:
            con6 = True

        if con0 & con1 & con2 & con3 & con4 & con5 & con6:
            return True
        else:
            return False

    def validar_id(self, id):
        return re.fullmatch(re.compile("\d+"), id.get()) != None
