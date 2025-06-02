import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

################################
# Creación del modelo de datos #
################################
"""
    MetaData se utiliza para almacenar información sobre la estructura de la base de datos, 
    mientras que declarative_base se utiliza para crear una clase base declarativa que 
    simplifica la definición de modelos de datos.
"""
# Crear una instancia de MetaData
# en metadata se va a ir creando la estructura de la base de datos
metadata = MetaData()

# Crear la clase de modelo utilizando Declarative Base
Base = declarative_base(metadata = metadata)

# Definir la clase de modelo para la tabla 'mi_tabla'
class Tabla_usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True, )
    nombre = Column(String(30), nullable=False)
    apellido1 = Column(String(30), nullable=False)
    apellido2 = Column(String(30), nullable=True)
    dni = Column(String(9), nullable=False, unique=True)
    date_created = Column(DateTime(), default = datetime.now(timezone.utc))

# OPCIONAL. Que la fecha de creación se actualice en el momento de insertar
# Definimos una función que se ejecutará antes de insertar un nuevo registro
def set_date_created(mapper, connection, target):
    if target.date_created is None:
        target.date_created = datetime.now(timezone.utc)

# Registramos el evento before_insert para la clase Tabla_Personas
event.listen(Tabla_usuario, 'before_insert', set_date_created)

"""
# Otra sintaxis, con un decorador
@event.listens_for(Tabla_Personas, 'before_insert')
def set_date_created(mapper, connection, target):
    if target.date_created is None:
        target.date_created = datetime.now(timezone.utc)
# Esto es equivalente a la función anterior.
"""

# La tabla vacía que hemos creado queda guardada en `metadata`
print(metadata.tables)
metadata.tables['tabla_personas']
metadata.tables['tabla_personas'].columns
metadata.tables['tabla_personas'].columns.keys()
metadata.tables['tabla_personas'].columns.values

# Crear el engine de SQLAlchemy para conectarse a la base de datos
engine = create_engine('sqlite:///biblioteca.db', echo=True)

# Crear la tabla (vacía) en la base de datos usando el engine
metadata.create_all(engine)
# Si la tabla ya existe, no se hace nada

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de cómo agregar un registro a la base de datos
# Nota: Si lo ejecuto dos veces la creación del mismo registro 
# da error porque dni ha de ser único
nuevo_registro = Tabla_usuario(nombre='Juan', apellido1='López', dni='12345678F')
# Puedo ver el contenido del registro.
# El id no está definido hasta que se añade el registro a la base de datos
nuevo_registro.id
# Tampoco date_created
nuevo_registro.date_created
nuevo_registro.nombre
nuevo_registro.apellido1
nuevo_registro.apellido2
nuevo_registro.dni
# El registro no se ha añadido a la base de datos hasta que se hace el commit
session.add(nuevo_registro)
session.commit()
