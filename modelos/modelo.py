import sys

sys.path.append("../library")
import re
from modelos.operaciones_base import DatabaseOps
from modelos.operaciones_data import DataOps


"""
modelo.py:
    Contiene las clases encargadas de administrar la conexión con la base de datos, la lógica interna del nuestra aplicación y funciones de validación de datos.
"""


class Modelo(DatabaseOps, DataOps):
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
            self.mostrar_mensaje_info("Su libro fue cargado correctamente")
            self.limpiar_y_armar(tree)
            self.blanquear_entradas(
                id, nombre, autor, editorial, año, categoria, estado
            )
        else:
            self.mostrar_mensaje_error(f"{mensaje_error}")

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
            answer = self.mostrar_pregunta_si_o_no(
                "¿Realmente desea eliminar este libro?"
            )
            if answer:
                self.baja_db(id.get())
                self.mostrar_mensaje_info("Su libro fue eliminado correctamente")
                self.limpiar_y_armar(tree)
                self.blanquear_entradas(
                    id, nombre, autor, editorial, año, categoria, estado
                )
        else:
            self.mostrar_mensaje_advertencia(
                f"El ID ingresado no es válido para ejecutar la acción.\n{mensaje_error}"
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
            answer = self.mostrar_pregunta_si_o_no(
                "¿Realmente desea modificar este libro?"
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
                self.mostrar_mensaje_info("Su libro fue modificado correctamente")
                self.limpiar_y_armar(tree)
                self.blanquear_entradas(
                    id, nombre, autor, editorial, año, categoria, estado
                )
        else:
            self.mostrar_mensaje_advertencia(
                f"Controle que todos los campos contengan datos válidos.\b{mensaje_error}"
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
