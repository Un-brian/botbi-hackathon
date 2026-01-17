"""
Script para poblar la base de datos con noticias
Obtiene desde scraper, procesa con IA y guarda en BD
"""

from backend.services.scraper import obtener_todas_las_noticias
from backend.services.ai_processor import procesar_noticia_completa
from backend.models import crear_noticia
import time

print("=" * 60)
print("🕸️  POBLANDO BASE DE DATOS")
print("=" * 60)

print("\n📡 Paso 1: Obteniendo noticias desde RSS feeds...")
resultado = obtener_todas_las_noticias(limite_por_categoria=3)

print(f"\n📊 Obtenidas: {resultado['total']} noticias sin procesar")
print(f"   - Tecnología: {len(resultado.get('Tecnología', []))}")
print(f"   - Negocios: {len(resultado.get('Negocios', []))}")

print("\n🤖 Paso 2: Procesando con IA y guardando en BD...")
print("⏱️  Esto tomará ~3 minutos (rate limit de Gemini)\n")

noticias_guardadas = 0
errores = 0

for categoria in ['Tecnología', 'Negocios']:
    noticias = resultado.get(categoria, [])
    
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
            
            # Esperar 3 segundos para no saturar Gemini
            if i < 3:  # No esperar después de la última
                print(f"        ⏳ Esperando 3s (rate limit)...")
                time.sleep(3)
            
        except Exception as e:
            errores += 1
            print(f"        ❌ Error: {e}")
            continue

print("\n" + "=" * 60)
print(f"✅ PROCESO COMPLETADO")
print(f"   Guardadas: {noticias_guardadas}")
print(f"   Errores: {errores}")
print("=" * 60)
print("\n💡 Ahora puedes ver las noticias en http://localhost:5000/api/news")
print("   O en tu frontend si está corriendo\n")