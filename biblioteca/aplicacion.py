from fastapi import FastAPI, HTTPException
import pickle
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone

app = FastAPI()

# Configuración de SQLAlchemy para conectar con biblioteca.db
engine = create_engine('sqlite:///biblioteca.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Modelo para la tabla usuario
class Tabla_usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    

def carga_datos():
    try:
        with open("publicaciones.pckl", 'rb') as archivo:
            publicaciones = pickle.load(archivo)
        return publicaciones
    except FileNotFoundError:
        return []

def guarda_datos(publicaciones):
    with open("publicaciones.pckl", 'wb') as archivo:
        pickle.dump(publicaciones, archivo)

publicaciones = carga_datos()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la biblioteca de libros"}

#preparar la apli para un GET una peticion a la base de datos
#preparar la aplicacion para un POST, una insercion de datos

@app.get("/listado")
def lee_listado():
    usuarios = session.query(Tabla_usuario).all()
    resultado = [
        {
            "id": u.id,
            "nombre": u.nombre,
            "apellido": u.apellido,
           
        }
        for u in usuarios
    ]
    return {"listado": resultado}

from uuid import uuid4

@app.post("/publicacion")
def guardar_publicacion(titulo: str,
                        contenido: str,
                        autor: str = "Aitor Donado"):
    nueva_publicacion = {
        "id": str(uuid4()),
        "titulo": titulo,
        "autor": autor,
        "contenido": contenido,
        "fecha_creacion": datetime.now().isoformat(),
        "fecha_publicacion": None
    }
    publicaciones.append(nueva_publicacion)
    guarda_datos(publicaciones)
    return nueva_publicacion

@app.get("/listado/{identificador}")
def lee_publicacion_id(identificador: str):
    for publicacion in publicaciones:
        if publicacion["id"] == identificador:
            return publicacion
    raise HTTPException(status_code=404,
                        detail="Publicación no encontrada")

@app.delete("/listado/{identificador}")
def elimina_publicacion_id(identificador: str):
    for indice, publicacion in enumerate(publicaciones):
        if publicacion["id"] == identificador:
            publicaciones.pop(indice)
            guarda_datos(publicaciones)
            return {"mensaje": "La publicación ha sido eliminada"}
    raise HTTPException(status_code=404,
                        detail="Publicación no encontrada")

@app.put("/listado/{identificador}")
def actualiza_publicacion_id(identificador: str,
                             titulo: str,
                             contenido: str,
                             autor: str = "Aitor Donado"):
    for publicacion in publicaciones:
        if publicacion["id"] == identificador:
            publicacion["titulo"] = titulo
            publicacion["contenido"] = contenido
            publicacion["autor"] = autor
            publicacion["fecha_publicacion"] = datetime.now().isoformat()
            guarda_datos(publicaciones)
            return {"mensaje": "La publicación ha sido actualizada"}
    raise HTTPException(status_code=404,
                        detail="Publicación no encontrada")