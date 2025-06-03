from sqlalchemy import create_engine
import psycopg2
import os
from dotenv import load_dotenv
import environ
from creartablas import UsuarioDB, MaterialDB, PrestamoDB




# Cargar variables de entorno
load_dotenv()
env = environ.Env()
env.read_env()

db_url = os.getenv('db_url_neon') or env('db_url_neon', default=None)
if not db_url:
    raise Exception('No se encontró la variable de entorno db_url_neon. Verifica tu archivo .env')
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
