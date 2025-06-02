from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from creartablas import UsuarioDB, MaterialDB, PrestamoDB

from datetime import datetime, timedelta

# Cambia esto si usas PostgreSQL:
connection_string = "postgresql://newlibrary_owner:npg_KrPkYAv7ShR8@ep-empty-lab-a9qveeyx-pooler.gwc.azure.neon.tech/newlibrary?sslmode=require"

# Crear engine y sesión
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
session = Session()

# 1. Crear y agregar un usuario
usuario = UsuarioDB(nombre="Juan", apellido="Pérez")
session.add(usuario)
session.commit()
usuarios_guardados = session.query(UsuarioDB).all()
for usuario in usuarios_guardados:
    print(f"Usuario añadido: {usuario.nombre} {usuario.apellido} (ID: {usuario.id_usuario})")

# 2. Crear y agregar un material
material = MaterialDB(
    codigo_inventario="ABC123",
    titulo="Cien Años de Soledad",
    tipo="libro",
    autor="Gabriel García Márquez",
    isbn="978-3-16-148410-0",
    numero_paginas=417,
    disponible=True
)
session.add(material)
session.commit()
materiales_guardados = session.query(MaterialDB).all()

for material in materiales_guardados:
    print(f"Material añadido: {material.titulo} (ID: {material.codigo_inventario})")

# 3. Crear y agregar un préstamo
prestamo = PrestamoDB(
    id_usuario=usuarios_guardados[0].id_usuario,
    id_material=materiales_guardados[0].codigo_inventario,
    fecha_prestamo=datetime.now(),
    fecha_devolucion=datetime.now() + timedelta(days=14)
)
session.add(prestamo)

# Marcar el material como no disponible
materiales_guardados[0].disponible = False

session.commit()

# 4. Verificar préstamo
prestamos = session.query(PrestamoDB).all()
print(f"\nTotal préstamos registrados: {len(prestamos)}")
for p in prestamos:
    print(f"- Usuario {p.id_usuario} → Material {p.id_material}, devuelve el {p.fecha_devolucion.date()}")