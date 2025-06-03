from fastapi import FastAPI, APIRouter
from biblioteca.gestorbiblioteca import GestorBiblioteca
from modelosBiblioteca import UsuarioDB, MaterialDB, PrestamoDB, UsuarioSchema, MaterialSchema, PrestamoSchema
from sqlalchemy.orm import declarative_base

Base = declarative_base()
app = FastAPI()
router = APIRouter()

@app.post("/usuarios/", response_model=UsuarioSchema)
def post_user(usuario: UsuarioSchema):
    gestor = GestorBiblioteca()
    id_usuario = gestor.agregar_usuario(usuario.nombre, usuario.apellido)
    return UsuarioSchema(id_usuario=id_usuario, nombre=usuario.nombre, apellido=usuario.apellido)

@app.get("/usuarios/", response_model=list[UsuarioSchema])
def get_users():
    gestor = GestorBiblioteca()
    usuarios = gestor.listar_usuarios()
    return [UsuarioSchema.from_orm(u) for u in usuarios]

@app.post("/materiales/", response_model=MaterialSchema)
def post_material(material: MaterialSchema):
    gestor = GestorBiblioteca()
    codigo = gestor.agregar_material(
        tipo=material.tipo,
        titulo=material.titulo,
        autor=material.autor,
        isbn=material.isbn,
        numero_paginas=material.numero_paginas,
        fecha_publicacion=material.fecha_publicacion,
        numero_edicion=material.numero_edicion,
        duracion=material.duracion,
        director=material.director
    )
    return MaterialSchema(codigo_inventario=codigo, **material.dict())

@app.post("/prestamos/", response_model=PrestamoSchema)
def post_prestamo(prestamo: PrestamoSchema):
    gestor = GestorBiblioteca()
    exito = gestor.agregar_prestamo(prestamo.id_usuario, prestamo.id_material)
    if exito:
        return prestamo
    else:
        return {"error": "No se pudo registrar el préstamo"}


