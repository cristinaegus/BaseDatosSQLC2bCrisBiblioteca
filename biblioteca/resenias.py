from pymongo import MongoClient
from pydantic import BaseModel, Field
from fastapi import Form
from datetime import datetime
from bson.objectid import ObjectId

import environ
env = environ.Env()
env.read_env(".env")
# Cadena de conexión de MongoDB Atlas
connection_string = env("connection_string")


# Conectar a la base de datos
client = MongoClient(connection_string)

# Verificar la conexión
try:
    # Listar las bases de datos disponibles
    databases = client.list_database_names()
    print("Conexión exitosa a MongoDB")
    print("Bases de datos disponibles:", databases)
except Exception as e:
    print("Error al conectar a MongoDB:", e)


db = client['MaterialBiblioteca_db']
collection = db['MaterialBiblioteca_collection']

class ReseniaMaterial(BaseModel):
    id_material: str = Field(alias="id_material")
    id_usuario: str = Field(alias="id_usuario")
    resenia: str = Field(alias="resenia")
    puntuacion: int = Field(alias="puntuacion")
    fecha: str = Field(alias="fecha")  # Cambiado a str

    @classmethod
    def as_form(cls, id_material: str = Form(...), id_usuario: str = Form(...), resenia: str = Form(...), puntuacion: int = Form(...), fecha: str = Form(...)):
        return cls(
            id_material=id_material,
            id_usuario=id_usuario,
            resenia=resenia,
            puntuacion=puntuacion,
            fecha=fecha
        )

def insertar_resenia_material(resenia_material: ReseniaMaterial):
    resenia_material_dict = resenia_material.dict(by_alias=True)
    # Guardar los IDs como string, no como ObjectId
    collection.insert_one(resenia_material_dict)

def listar_resenias():
    return list(collection.find({}, {"_id": 0}))