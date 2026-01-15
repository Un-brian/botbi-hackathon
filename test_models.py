"""
Script para listar modelos disponibles en tu API Key
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY no encontrada")
    exit(1)

print(f"✅ API Key: {api_key[:10]}...\n")

genai.configure(api_key=api_key)

print("📋 Modelos disponibles:\n")

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  ✅ {model.name}")
            print(f"     Descripción: {model.display_name}")
            print()
except Exception as e:
    print(f"❌ Error: {e}")