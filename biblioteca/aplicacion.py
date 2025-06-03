from fastapi import FastAPI, HTTPException
import pickle

app = FastAPI()

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
    return {"listado": publicaciones}

from uuid import uuid4
from datetime import datetime

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