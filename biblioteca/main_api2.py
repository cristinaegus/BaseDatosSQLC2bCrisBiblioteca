from fastapi import FastAPI, APIRouter, Form, Query, HTTPException, Depends
from pydantic import BaseModel
from biblioteca.gestorbiblioteca import GestorBiblioteca
from creartablas import UsuarioDB, MaterialDB, PrestamoDB
from sqlalchemy.orm import declarative_base
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware



Base = declarative_base()
app = FastAPI() 
router = APIRouter()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

biblioteca = GestorBiblioteca()


# Modelos Pydantic
class UsuarioIn(BaseModel):
    nombre: str
    apellido: str

    @classmethod
    def as_form(cls, nombre: str = Form(...), apellido: str = Form(...)):
        return cls(nombre=nombre, apellido=apellido)

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

    @classmethod
    def as_form(
        cls,
        tipo: str = Form(...),
        titulo: str = Form(...),
        autor: str = Form(None),
        isbn: str = Form(None),
        numero_paginas: int = Form(None),
        fecha_publicacion: str = Form(None),
        numero_edicion: str = Form(None),
        duracion: int = Form(None),
        director: str = Form(None),
    ):
        return cls(
            tipo=tipo,
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            numero_paginas=numero_paginas,
            fecha_publicacion=fecha_publicacion,
            numero_edicion=numero_edicion,
            duracion=duracion,
            director=director,
        )

class PrestamoIn(BaseModel):
    id_usuario: str
    id_material: str
    fecha_prestamo: str
    fecha_devolucion: str

    @classmethod
    def as_form(
        cls,
        id_usuario: str = Form(...),
        id_material: str = Form(...),
        fecha_prestamo: str = Form(...),
        fecha_devolucion: str = Form(...),
    ):
        return cls(
            id_usuario=id_usuario,
            id_material=id_material,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion=fecha_devolucion,
        )

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
def post_user(usuario: UsuarioIn = Depends(UsuarioIn.as_form)):
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
def post_material(material: MaterialIn = Depends(MaterialIn.as_form)):
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
def post_prestamo(prestamo: PrestamoIn = Depends(PrestamoIn.as_form)):
    # Validación de fechas usando el método del modelo
    try:
        PrestamoIn.validate_dates(prestamo.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    gestor = GestorBiblioteca()
    exito = gestor.agregar_prestamo(prestamo.id_usuario, prestamo.id_material)
    if exito:
        return {
            "id_usuario": prestamo.id_usuario,
            "id_material": prestamo.id_material,
            "fecha_prestamo": prestamo.fecha_prestamo,
            "fecha_devolucion": prestamo.fecha_devolucion
        }
    else:
        raise HTTPException(status_code=400, detail="No se pudo registrar el préstamo")

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

@app.delete("/usuarios/{id_usuario}")
def delete_usuario(id_usuario: str):
    gestor = GestorBiblioteca()
    exito = gestor.borrar_usuario(id_usuario)
    if exito:
        return {"mensaje": f"Usuario {id_usuario} eliminado correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/materiales/{codigo_inventario}")
def delete_material(codigo_inventario: str):
    gestor = GestorBiblioteca()
    exito = gestor.borrar_material(codigo_inventario)
    if exito:
        return {"mensaje": f"Material {codigo_inventario} eliminado correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Material no encontrado")



