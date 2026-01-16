"""
Script de prueba para el procesador de IA
"""

from backend.services.ai_processor import (
    reescribir_noticia,
    generar_resumen,
    extraer_puntos_clave,
    procesar_noticia_completa
)

print("=" * 60)
print("🧪 PRUEBA DEL PROCESADOR DE IA")
print("=" * 60)

# Noticia de prueba
titulo_original = "Apple lanza nuevo iPhone 15 con mejoras en cámara"
contenido_original = """
Apple presentó hoy su nuevo iPhone 15 en un evento especial en Cupertino, California. 
El dispositivo cuenta con importantes mejoras en el sistema de cámaras, incluyendo un 
nuevo sensor de 48 megapíxeles y capacidades mejoradas para fotografía nocturna. 
Además, la batería ofrece hasta 20 horas de reproducción de video, un incremento del 
15% respecto al modelo anterior. El iPhone 15 estará disponible a partir del 22 de 
septiembre con precios desde $799 USD.
"""
categoria = "Tecnología"

print("\n📰 NOTICIA ORIGINAL:")
print(f"Título: {titulo_original}")
print(f"Contenido: {contenido_original[:100]}...")

print("\n🔄 Procesando con IA...\n")

# Prueba 1: Reescribir noticia
print("1️⃣  REESCRITURA:")
resultado = reescribir_noticia(titulo_original, contenido_original, categoria)
print(f"Título nuevo: {resultado['titulo']}")
print(f"Contenido nuevo: {resultado['contenido'][:150]}...")
print(f"Exitoso: {'✅' if resultado['exitoso'] else '❌'}")

print("\n" + "-" * 60)

# Prueba 2: Generar resumen
print("\n2️⃣  RESUMEN:")
resumen = generar_resumen(contenido_original, max_palabras=30)
print(f"{resumen}")

print("\n" + "-" * 60)

# Prueba 3: Extraer puntos clave
print("\n3️⃣  PUNTOS CLAVE:")
puntos = extraer_puntos_clave(contenido_original, num_puntos=3)
for i, punto in enumerate(puntos, 1):
    print(f"   {i}. {punto}")

print("\n" + "-" * 60)

# Prueba 4: Procesamiento completo
print("\n4️⃣  PROCESAMIENTO COMPLETO:")
resultado_completo = procesar_noticia_completa(titulo_original, contenido_original, categoria)

print(f"\n📌 Título: {resultado_completo['titulo']}")
print(f"\n📄 Contenido:\n{resultado_completo['contenido']}")
print(f"\n📝 Resumen: {resultado_completo['resumen']}")
print(f"\n🔑 Puntos clave:")
for i, punto in enumerate(resultado_completo['puntos_clave'], 1):
    print(f"   {i}. {punto}")

print("\n" + "=" * 60)
print("✅ Prueba completada")
print("=" * 60)