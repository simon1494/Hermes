import sys

sys.path.append("../library")
import pandas as pd
from clases.patron_observador import Sujeto
from clases.estructura_base import Libro
from clases.cuadros_de_dialogo import Mensajes
from clases.cuadros_de_dialogo import mensaje_operacion


class Modelo(Mensajes, Sujeto):
    def __init__(self, base_de_datos):
        self.db = base_de_datos
        self.crear_db()

    def crear_db(self):
        """
        Crea una base de datos donde se almacenará la información de nuestra aplicación. La función se ejecuta cada vez que la aplicación es abierta, pero en el caso de que ya exista una base creada, entonces no tendrá ningún efecto.
        """
        try:
            self.db.connect()
            self.db.create_tables([Libro])
        except Exception as error:
            self.db.mostrar_mensaje_error(f"Error creando base de datos: {error}")

    @mensaje_operacion("alta")
    def alta_db(self, nombre, autor, editorial, año, categoria, estado):
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
        self.notificar_a_observadores()

    @mensaje_operacion("baja")
    def baja_db(self, id):
        """
        Genera la baja de un registro en la base de datos de nuestra aplicación.

        :param id: Integer. ID del libro que se desea eliminar."""
        registro = Libro.get(Libro.id == id)
        registro.delete_instance()
        self.notificar_a_observadores()

    @mensaje_operacion("mod")
    def modificar_db(self, id, nombre, autor, editorial, año, categoria, estado):
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
        print("entre")
        registro = Libro.update(
            nombre=nombre,
            autor=autor,
            editorial=editorial,
            año=año,
            categoria=categoria,
            estado=estado,
        ).where(Libro.id == id)
        registro.execute()
        self.notificar_a_observadores()

    def consultar_db(self, sobre, clausula, df, item):
        """
        Actualiza el Treeview de nuestra aplicación con el resultado consulta sobre el campo que elijamos.

        :param sobre: String. Determina sobre qué campo de nuestra base se ejecutará la consulta. Por default None, lo que establece una busqueda de todos los registros.
        :param clausula: String. Determina la expresión a matchear en los registros del campo seleccionado. Por default None, lo que establece una busqueda sin criterio.
        :param df: Booleano. Determina si el resultado de la consulta en base de regresa en formado dataframe o lista. Por default en True (devuelve dataframe)
        :return: Datos de consulta en formato dataframe o lista"""
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
        final = self._convertir_query(resultado, df, item)

        return final

    @staticmethod
    def _convertir_query(resultado, df, item=False):
        """
        Convierte el resultado de una consulta a base en dataframe o lista según corresponda.

        :param resultado: Objeto propio del ORM Peewee. Es el resultado de una consulta.
        :param df: Booleano. Seteado en True convierte el resultado en dataframe; de lo contrario, lista.
        :return: Dataframe o lista. Resultado de la consulta a base convertido en formato conveniente.
        """
        if item:
            resultado_ = Libro.select().where(Libro.id == resultado)
            final = []
            for registro in resultado_:
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
        else:
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
