"""
Script de prueba para verificar que Gemini funciona
"""

import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import os

# Cargo variables de entorno (forzando la ruta)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Verifico que se cargó
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY no encontrada en .env")
    print(f"Buscando en: {env_path.absolute()}")
    print(f"¿Existe el archivo? {env_path.exists()}")
    exit(1)

print(f"✅ API Key encontrada: {api_key[:10]}...")

# Configuro Gemini
genai.configure(api_key=api_key)

# Creo el modelo (usando el que tienes disponible)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# Prueba simple
print("\n🧪 Probando conexión con Gemini...\n")

prompt = """
Reescribe esta noticia de forma original, manteniendo los hechos pero usando tus propias palabras:

"Apple lanzó hoy su nuevo iPhone 15 con mejoras significativas en la cámara y batería de mayor duración."
"""

try:
    response = model.generate_content(prompt)
    print("✅ Respuesta de Gemini:")
    print("-" * 60)
    print(response.text)
    print("-" * 60)
    print("\n🎉 ¡Gemini está funcionando correctamente!")
except Exception as e:
    print(f"❌ Error al conectar con Gemini: {e}")