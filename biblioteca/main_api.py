from fastapi import FastAPI, APIRouter, Form, Query
from biblioteca.gestorbiblioteca import GestorBiblioteca
from modelosBiblioteca import UsuarioDB, MaterialDB, PrestamoDB
from sqlalchemy.orm import declarative_base

Base = declarative_base()
app = FastAPI() 
router = APIRouter()

@app.post("/usuarios/")
def post_user(nombre: str = Form(...), apellido: str = Form(...)):
    gestor = GestorBiblioteca()
    id_usuario = gestor.agregar_usuario(nombre, apellido)
    return {"id_usuario": id_usuario, "nombre": nombre, "apellido": apellido}

@app.get("/usuarios/")
def get_users():
    gestor = GestorBiblioteca()
    usuarios = gestor.listar_usuarios()
    return [
        {"id_usuario": u.id_usuario, "nombre": u.nombre, "apellido": u.apellido}
        for u in usuarios
    ]

@app.post("/materiales/")
def post_material(
    tipo: str = Form(...),
    titulo: str = Form(...),
    autor: str = Form(None),
    isbn: str = Form(None),
    numero_paginas: int = Form(None),
    fecha_publicacion: str = Form(None),
    numero_edicion: str = Form(None),
    duracion: int = Form(None),
    director: str = Form(None)
):
    gestor = GestorBiblioteca()
    codigo = gestor.agregar_material(
        tipo=tipo,
        titulo=titulo,
        autor=autor,
        isbn=isbn,
        numero_paginas=numero_paginas,
        fecha_publicacion=fecha_publicacion,
        numero_edicion=numero_edicion,
        duracion=duracion,
        director=director
    )
    return {
        "codigo_inventario": codigo,
        "tipo": tipo,
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,
        "numero_paginas": numero_paginas,
        "fecha_publicacion": fecha_publicacion,
        "numero_edicion": numero_edicion,
        "duracion": duracion,
        "director": director
    }

@app.post("/prestamos/")
def post_prestamo(
    id_usuario: str = Form(...),
    id_material: str = Form(...)
):
    gestor = GestorBiblioteca()
    exito = gestor.agregar_prestamo(id_usuario, id_material)
    if exito:
        return {"id_usuario": id_usuario, "id_material": id_material}
    else:
        return {"error": "No se pudo registrar el préstamo"}


