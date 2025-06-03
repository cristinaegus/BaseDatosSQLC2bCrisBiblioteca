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

# 1. Crear y agregar usuarios
usuario1 = UsuarioDB(nombre="Juan", apellido="Pérez")
usuario2 = UsuarioDB(nombre="Cristina", apellido="Gómez")
session.add_all([usuario1, usuario2])
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

def menu():
    while True:
        print("\n--- Menú Biblioteca ---")
        print("1. Crear usuario")
        print("2. Agregar material")
        print("3. Crear préstamo")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            usuario = UsuarioDB(nombre=nombre, apellido=apellido)
            session.add(usuario)
            session.commit()
            print(f"Usuario añadido: {usuario.nombre} {usuario.apellido} (ID: {usuario.id_usuario})")
        elif opcion == "2":
            codigo = input("Código inventario: ")
            titulo = input("Título: ")
            tipo = input("Tipo (libro/revista/dvd): ")
            autor = input("Autor: ") if tipo == "libro" else None
            isbn = input("ISBN: ") if tipo == "libro" else None
            numero_paginas = int(input("Número de páginas: ")) if tipo == "libro" else None
            fecha_publicacion = input("Fecha publicación: ") if tipo == "revista" else None
            numero_edicion = input("Número edición: ") if tipo == "revista" else None
            duracion = int(input("Duración (min): ")) if tipo == "dvd" else None
            director = input("Director: ") if tipo == "dvd" else None
            material = MaterialDB(
                codigo_inventario=codigo,
                titulo=titulo,
                tipo=tipo,
                autor=autor,
                isbn=isbn,
                numero_paginas=numero_paginas,
                fecha_publicacion=fecha_publicacion,
                numero_edicion=numero_edicion,
                duracion=duracion,
                director=director,
                disponible=True
            )
            session.add(material)
            session.commit()
            print(f"Material añadido: {material.titulo} (ID: {material.codigo_inventario})")
        elif opcion == "3":
            usuarios = session.query(UsuarioDB).all()
            materiales = session.query(MaterialDB).filter_by(disponible=True).all()
            if not usuarios or not materiales:
                print("Debe haber al menos un usuario y un material disponible.")
                continue
            print("Usuarios disponibles:")
            for u in usuarios:
                print(f"{u.id_usuario}: {u.nombre} {u.apellido}")
            id_usuario = input("ID usuario: ")
            print("Materiales disponibles:")
            for m in materiales:
                print(f"{m.codigo_inventario}: {m.titulo}")
            id_material = input("Código inventario material: ")
            prestamo = PrestamoDB(
                id_usuario=id_usuario,
                id_material=id_material,
                fecha_prestamo=datetime.now(),
                fecha_devolucion=datetime.now() + timedelta(days=14)
            )
            session.add(prestamo)
            # Marcar material como no disponible
            material = session.query(MaterialDB).filter_by(codigo_inventario=id_material).first()
            if material:
                material.disponible = False
            session.commit()
            print("Préstamo creado correctamente.")
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()