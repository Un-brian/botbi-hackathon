"""
Script para poblar la base de datos con noticias
Obtiene desde scraper, procesa con IA y guarda en BD
"""

import sys
import os
import time

# Asegurar que Python encuentre los módulos si se ejecuta desde terminal
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.services.scraper import obtener_todas_las_noticias
from backend.services.ai_processor import procesar_noticia_completa
from backend.models import crear_noticia, init_db # <--- AGREGADO init_db

print("=" * 60)
print("🕸️  POBLANDO BASE DE DATOS (MODO DEMO)")
print("=" * 60)

# 1. Asegurar que las tablas existan
print("🛠️  Verificando estructura de base de datos...")
init_db() # <--- ESTA ES LA LÍNEA CRÍTICA
print("   ✅ Base de datos lista.")

print("\n📡 Paso 1: Obteniendo noticias desde RSS feeds...")
try:
    resultado = obtener_todas_las_noticias(limite_por_categoria=3)
except Exception as e:
    print(f"❌ Error conectando a fuentes RSS: {e}")
    sys.exit(1)

print(f"\n📊 Obtenidas: {resultado['total']} noticias sin procesar")
print(f"   - Tecnología: {len(resultado.get('Tecnología', []))}")
print(f"   - Negocios: {len(resultado.get('Negocios', []))}")

print("\n🤖 Paso 2: Procesando con IA y guardando en BD...")
print("⏱️  Esto tomará unos minutos (respetando límites de Gemini API)...\n")

noticias_guardadas = 0
errores = 0

for categoria in ['Tecnología', 'Negocios']:
    noticias = resultado.get(categoria, [])
    
    if not noticias:
        continue

    print(f"\n📁 Procesando categoría: {categoria}")
    
    for i, noticia in enumerate(noticias[:3], 1):  # Solo 3 por categoría
        try:
            print(f"   [{i}/3] {noticia['titulo'][:50]}...")
            
            # Procesar con IA
            procesado = procesar_noticia_completa(
                noticia['titulo'],
                noticia['contenido'],
                categoria
            )
            
            if procesado['exitoso']:
                # Guardar en BD
                crear_noticia(
                    titulo=procesado['titulo'],
                    contenido=procesado['contenido'],
                    categoria=categoria,
                    fuente_original=noticia.get('fuente_original')
                )
                
                noticias_guardadas += 1
                print(f"        ✅ Guardada ({noticias_guardadas} total)")
            else:
                errores += 1
                print(f"        ⚠️  Error al procesar con IA")
            
            # Esperar 4 segundos (Seguridad extra para la API key nueva)
            if i < 3: 
                print(f"        ⏳ Esperando 4s...")
                time.sleep(4)
            
        except Exception as e:
            errores += 1
            print(f"        ❌ Error: {e}")
            continue

print("\n" + "=" * 60)
print(f"✅ PROCESO COMPLETADO")
print(f"   Guardadas: {noticias_guardadas}")
print(f"   Errores: {errores}")
print("=" * 60)
print("\n💡 Ahora ejecuta: python app.py")