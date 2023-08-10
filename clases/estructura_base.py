import peewee as pw

DB = pw.SqliteDatabase("biblioteca.db")


class ModeloBase(pw.Model):
    """
    Clase que defina la base de datos para el ORM.
    """

    class Meta:
        """.. sphinx-autodoc-skip::"""

        database = DB


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
