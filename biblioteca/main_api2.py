from fastapi import FastAPI, APIRouter, Form, Query
from pydantic import BaseModel
from biblioteca.gestorbiblioteca import GestorBiblioteca
from creartablas import UsuarioDB, MaterialDB, PrestamoDB
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()
app = FastAPI() 
router = APIRouter()

# Modelos Pydantic
class UsuarioIn(BaseModel):
    nombre: str
    apellido: str

class MaterialIn(BaseModel):
    tipo: str
    titulo: str
    autor: str | None = None
    isbn: str | None = None
    numero_paginas: int | None = None
    fecha_publicacion: str | None = None
    numero_edicion: str | None = None
    duracion: int | None = None
    director: str | None = None

class PrestamoIn(BaseModel):
    id_usuario: str
    id_material: str
    fecha_prestamo: str
    fecha_devolucion: str

    @classmethod
    def validate_dates(cls, values):
        try:
            fecha_prestamo = datetime.fromisoformat(values['fecha_prestamo'])
            fecha_devolucion = datetime.fromisoformat(values['fecha_devolucion'])
            if fecha_devolucion <= fecha_prestamo:
                raise ValueError('La fecha de devolución debe ser posterior a la fecha de préstamo')
        except Exception as e:
            raise ValueError(f'Error en las fechas: {e}')
        return values

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        @staticmethod
        def schema_extra(schema, model):
            schema['example'] = {
                "id_usuario": "ABC123",
                "id_material": "XYZ789",
                "fecha_prestamo": "2025-06-04T10:00:00",
                "fecha_devolucion": "2025-06-18T10:00:00"
            }

    # Validación automática al crear la instancia
    def __init__(self, **data):
        super().__init__(**data)
        PrestamoIn.validate_dates(self.dict())

@app.post("/usuarios/")
def post_user(usuario: UsuarioIn):
    gestor = GestorBiblioteca()
    id_usuario = gestor.agregar_usuario(usuario.nombre, usuario.apellido)
    return {"id_usuario": id_usuario, "nombre": usuario.nombre, "apellido": usuario.apellido}

@app.get("/usuarios/")
def get_users():
    gestor = GestorBiblioteca()
    usuarios = gestor.listar_usuarios()
    return [
        {"id_usuario": u.id_usuario, "nombre": u.nombre, "apellido": u.apellido}
        for u in usuarios
    ]

@app.post("/materiales/")
def post_material(material: MaterialIn):
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
    return {
        "codigo_inventario": codigo,
        **material.dict()
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
def post_prestamo(prestamo: PrestamoIn):
    # Validación de fechas ya realizada en el modelo
    gestor = GestorBiblioteca()
    exito = gestor.agregar_prestamo(prestamo.id_usuario, prestamo.id_material)
    if exito:
        return prestamo
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



