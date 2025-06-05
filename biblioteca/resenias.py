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
    fecha: datetime = Field(alias="fecha")

    @classmethod
    def as_form(cls, id_material: str = Form(...), id_usuario: str = Form(...), resenia: str = Form(...), puntuacion: int = Form(...), fecha: datetime = Form(...)):
        return cls(
            id_material=id_material,
            id_usuario=id_usuario,
            resenia=resenia,
            puntuacion=puntuacion,
            fecha=fecha
        )

def insertar_resenia_material(resenia_material: ReseniaMaterial):
    resenia_material_dict = resenia_material.dict(by_alias=True)
    try:
        resenia_material_dict['id_material'] = ObjectId(resenia_material_dict['id_material'])
        resenia_material_dict['id_usuario'] = ObjectId(resenia_material_dict['id_usuario'])
    except Exception as e:
        raise ValueError("El id_material o id_usuario no tiene formato válido de ObjectId") from e
    collection.insert_one(resenia_material_dict)

nueva_resenia = {
    "autor": "55E58A",
    "material": "ABC123",
    "resenia": "Muy buen libro. Me ha gustado",
    "mencionar_usuarios": ["B6EDE9"],
    "calificacion": 5,
    "fecha": ""
}   

nueva_resenia = {
    "autor": "55E58A",
    "material": "ABC123",
    "resenia": "Muy buen libro. Me ha gustado",
    "mencionar_usuarios": ["B6EDE9"],
    "calificacion": 5,
    "fecha": ""
}   

collection.insert_one(nueva_resenia)

def listar_resenias():
    return list(collection.find({"autor": "55E58A", "material": "ABC123"}))

lista_resenias = listar_resenias()
print(lista_resenias)

# Todos los documentos
for usuario in db.resenias.find():
    print(usuario)


def borrar_resenia(autor, material):
    collection.delete_one({"autor": autor, "material": material})
    return "Resenia borrada correctamente"
borrar = borrar_resenia("55E58A", "ABC123")
print(borrar)  # Debería imprimir "Resenia borrada correctamente" si se borró correctamente