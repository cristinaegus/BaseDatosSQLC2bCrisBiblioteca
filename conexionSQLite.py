"""
Conexión a una base de datos sqlite local
que almacena los datos en el archivo ejemplo.db
"""
from sqlalchemy import create_engine

# Definir la URL de conexión a la base de datos
# SQLite crea la base de datos en un archivo local
db_url = 'sqlite:///ejemplo.db'

# Crear una instancia de motor (engine)
engine = create_engine(db_url)

# Realizar una conexión a la base de datos
try:
    # Intentar conectarse a la base de datos
    connection = engine.connect()
    print("Conexión exitosa")

    # Aquí puedes realizar operaciones en la base de datos

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión cuando hayas terminado
    if connection:
        print("Cerrando la conexión")
        connection.close()