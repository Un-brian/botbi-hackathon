"""
Script de prueba para la Base de Datos (SQLite)
Verifica que se puedan guardar y leer noticias
"""

import os
from backend.models import init_db, crear_noticia, obtener_todas_noticias, get_db_connection

# Asegurar que usamos una BD de prueba o la local
print("=" * 60)
print("🗄️  PRUEBA DE BASE DE DATOS")
print("=" * 60)

# 1. Inicializar DB
print("\n🛠️  Inicializando base de datos...")
try:
    init_db()
    print("✅ Tablas creadas correctamente.")
except Exception as e:
    print(f"❌ Error al inicializar DB: {e}")
    exit(1)

# 2. Crear una noticia de prueba
print("\n📝 Creando noticia de prueba...")
titulo = "Test Unitario DB"
contenido = "Esta es una noticia de prueba para verificar la persistencia de datos."
categoria = "Tecnología"

try:
    resultado = crear_noticia(
        titulo=titulo,
        contenido=contenido,
        categoria=categoria,
        fuente_original="localhost"
    )
    print(f"✅ Noticia creada con ID: {resultado['id']}")
except Exception as e:
    print(f"❌ Error al crear noticia: {e}")

# 3. Leer noticias
print("\n📖 Leyendo noticias de la BD...")
try:
    noticias = obtener_todas_noticias()
    encontrada = False
    for n in noticias:
        if n['titulo'] == titulo:
            print(f"✅ Noticia encontrada en BD: {n['titulo']}")
            print(f"   Fecha: {n['fecha']}")
            encontrada = True
            break
    
    if not encontrada:
        print("❌ La noticia creada no aparece en la consulta.")

except Exception as e:
    print(f"❌ Error al leer noticias: {e}")

print("\n" + "=" * 60)
print("✅ PRUEBA DE MODELOS COMPLETADA")
print("=" * 60)