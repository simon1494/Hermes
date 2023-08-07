import sys

sys.path.append("../library")
import pandas as pd
from modelos.estructura_base import DB
from modelos.estructura_base import Libro
from modelos.cuadros_de_dialogo import Mensajes


class DatabaseOps(Mensajes):
    @classmethod
    def crear_db(cls):
        """
        Crea una base de datos donde se almacenará la información de nuestra aplicación. La función se ejecuta cada vez que la aplicación es abierta, pero en el caso de que ya exista una base creada, entonces no tendrá ningún efecto.
        """
        try:
            DB.connect()
            DB.create_tables([Libro])
        except Exception as error:
            cls.mostrar_mensaje_error(f"Error creando base de datos: {error}")



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