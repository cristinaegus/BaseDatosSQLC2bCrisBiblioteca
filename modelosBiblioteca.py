from sqlalchemy import create_engine
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# URL de conexión a la base de datos PostgreSQL en el archivo .env
import environ
env = environ.Env()
env.read_env(".env")
db_url = env("db_url")
print("Comprobamos que ha tomado el valor de la variable de entorno:", db_url)

# Si se quiere usar SQLite en lugar de la base remota:


# Obtener la URL de la base de datos desde la variable de entorno
DB_URL = os.getenv('db_url_neon')

# Crear conexión y cursor para ejecutar las sentencias de creación de tablas
def crear_tablas():
    connection = None
    try:
        connection = psycopg2.connect(DB_URL)
        cursor = connection.cursor()
        # ...existing code...
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Crear una instancia de motor (engine)
engine = create_engine(db_url)
