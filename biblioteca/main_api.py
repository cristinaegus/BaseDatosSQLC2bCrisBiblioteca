from fastapi import FastAPI, APIRouter, Form, Query, Depends, HTTPException
from biblioteca.gestorbiblioteca import GestorBiblioteca
from creartablas import UsuarioDB, MaterialDB, PrestamoDB
from sqlalchemy.orm import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

Base = declarative_base()
app = FastAPI() 
router = APIRouter()

app.get("/")
def root():
    return {"message": "API Biblioteca funcionando. Visita /docs para la documentación."}
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

biblioteca = GestorBiblioteca()

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
@app.get("/materiales/")
def get_materials():
    gestor = GestorBiblioteca()
    materiales = gestor.listar_materiales()
    return [
        {
            "codigo_inventario": m.codigo_inventario,
            "tipo": m.tipo,
            "titulo": m.titulo,
            "autor": m.autor,
            "isbn": m.isbn,
            "numero_paginas": m.numero_paginas,
            "fecha_publicacion": m.fecha_publicacion,
            "numero_edicion": m.numero_edicion,
            "duracion": m.duracion,
            "director": m.director
        }
        for m in materiales
    ]   

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
@app.get("/prestamos/")
def get_prestamos():
    gestor = GestorBiblioteca()
    prestamos = gestor.listar_prestamos()
    return [
        {
            "id_usuario": p.id_usuario,
            "id_material": p.id_material,
            "fecha_prestamo": p.fecha_prestamo.isoformat(),
            "fecha_devolucion": p.fecha_devolucion.isoformat()
        }
        for p in prestamos
    ]





