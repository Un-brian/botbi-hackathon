"""
Procesador de IA - Integración con Google Gemini
Reescribe noticias para hacerlas originales y genera contenido procesado
"""

import google.generativeai as genai
from backend.config import Config
import time

# Configuro Gemini con la API key
genai.configure(api_key=Config.GEMINI_API_KEY)

# Creo el modelo (uso el configurado en config.py)
model = genai.GenerativeModel(Config.GEMINI_MODEL)


def reescribir_noticia(titulo_original, contenido_original, categoria):
    """
    Reescribe una noticia usando IA para hacerla original
    
    Args:
        titulo_original (str): Título de la noticia original
        contenido_original (str): Contenido de la noticia original
        categoria (str): Categoría de la noticia (Tecnología, Negocios, Mercados)
    
    Returns:
        dict: {
            'titulo': str,
            'contenido': str,
            'exitoso': bool
        }
    """
    try:
        prompt = f"""
Actúo como redactor profesional de noticias. Mi tarea es reescribir la siguiente noticia de forma COMPLETAMENTE ORIGINAL, manteniendo todos los hechos pero usando mis propias palabras, estructura y estilo.

**Categoría:** {categoria}

**Título original:** {titulo_original}

**Contenido original:**
{contenido_original}

**Instrucciones:**
1. Reescribe el título de forma atractiva y original
2. Reescribe el contenido completo usando tus propias palabras
3. Mantén TODOS los hechos, datos y cifras exactos
4. Usa un estilo periodístico profesional
5. Extensión: 2-3 párrafos (150-250 palabras)
6. NO uses comillas ni cites el texto original
7. Escribe en español

**Formato de respuesta:**
TÍTULO: [tu título reescrito]

CONTENIDO: [tu contenido reescrito]
"""
        
        # Genero el contenido con Gemini
        response = model.generate_content(prompt)
        texto_completo = response.text
        
        # Extraigo título y contenido de la respuesta
        titulo_reescrito = ""
        contenido_reescrito = ""
        
        if "TÍTULO:" in texto_completo and "CONTENIDO:" in texto_completo:
            partes = texto_completo.split("CONTENIDO:")
            titulo_parte = partes[0].replace("TÍTULO:", "").strip()
            contenido_parte = partes[1].strip()
            
            titulo_reescrito = titulo_parte
            contenido_reescrito = contenido_parte
        else:
            # Si no sigue el formato, uso el texto completo como contenido
            # y genero un título simple
            contenido_reescrito = texto_completo.strip()
            titulo_reescrito = _generar_titulo_simple(contenido_reescrito)
        
        return {
            'titulo': titulo_reescrito,
            'contenido': contenido_reescrito,
            'exitoso': True
        }
        
    except Exception as e:
        print(f"❌ Error al reescribir noticia: {e}")
        return {
            'titulo': titulo_original,
            'contenido': contenido_original,
            'exitoso': False
        }


def generar_resumen(contenido, max_palabras=50):
    """
    Genera un resumen corto de una noticia (para newsletter)
    
    Args:
        contenido (str): Contenido completo de la noticia
        max_palabras (int): Máximo de palabras del resumen
    
    Returns:
        str: Resumen generado
    """
    try:
        prompt = f"""
Resume esta noticia en máximo {max_palabras} palabras, manteniendo lo más importante:

{contenido}

Instrucciones:
- Máximo {max_palabras} palabras
- Mantén los datos clave
- Estilo directo y claro
- Una sola oración o párrafo corto
"""
        
        response = model.generate_content(prompt)
        resumen = response.text.strip()
        
        return resumen
        
    except Exception as e:
        print(f"❌ Error al generar resumen: {e}")
        # Fallback: tomo las primeras palabras del contenido
        palabras = contenido.split()
        return ' '.join(palabras[:max_palabras]) + '...'


def extraer_puntos_clave(contenido, num_puntos=3):
    """
    Extrae los puntos más importantes de una noticia
    
    Args:
        contenido (str): Contenido completo de la noticia
        num_puntos (int): Número de puntos clave a extraer
    
    Returns:
        list: Lista de puntos clave
    """
    try:
        prompt = f"""
Extrae los {num_puntos} puntos más importantes de esta noticia:

{contenido}

Instrucciones:
- Exactamente {num_puntos} puntos
- Cada punto en una línea
- Formato: "- Punto 1"
- Conciso y directo
"""
        
        response = model.generate_content(prompt)
        texto = response.text.strip()
        
        # Extraigo los puntos (busco líneas que empiecen con -, *, o números)
        puntos = []
        for linea in texto.split('\n'):
            linea = linea.strip()
            if linea and (linea.startswith('-') or linea.startswith('*') or linea[0].isdigit()):
                # Limpio el formato
                punto_limpio = linea.lstrip('-*0123456789. ').strip()
                if punto_limpio:
                    puntos.append(punto_limpio)
        
        return puntos[:num_puntos]
        
    except Exception as e:
        print(f"❌ Error al extraer puntos clave: {e}")
        return []


def _generar_titulo_simple(contenido):
    """
    Genera un título simple a partir del contenido
    Función auxiliar interna
    """
    try:
        prompt = f"""
Genera un título atractivo y corto (máximo 10 palabras) para esta noticia:

{contenido[:200]}...

Solo responde con el título, nada más.
"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except:
        # Si falla, tomo las primeras palabras
        palabras = contenido.split()
        return ' '.join(palabras[:8])


def procesar_noticia_completa(titulo_original, contenido_original, categoria):
    """
    Procesa una noticia completa: reescribe, genera resumen y extrae puntos clave
    Función todo-en-uno para facilitar el uso
    
    Args:
        titulo_original (str): Título original
        contenido_original (str): Contenido original
        categoria (str): Categoría de la noticia
    
    Returns:
        dict: {
            'titulo': str,
            'contenido': str,
            'resumen': str,
            'puntos_clave': list,
            'exitoso': bool
        }
    """
    # Reescribo la noticia
    resultado_reescritura = reescribir_noticia(titulo_original, contenido_original, categoria)
    
    if not resultado_reescritura['exitoso']:
        return {
            'titulo': titulo_original,
            'contenido': contenido_original,
            'resumen': '',
            'puntos_clave': [],
            'exitoso': False
        }
    
    # Espero un poco para no saturar la API (rate limiting)
    time.sleep(3)
    
    # Genero resumen
    resumen = generar_resumen(resultado_reescritura['contenido'])
    
    # Espero un poco más
    time.sleep(3)
    
    # Extraigo puntos clave
    puntos_clave = extraer_puntos_clave(resultado_reescritura['contenido'])
    
    return {
        'titulo': resultado_reescritura['titulo'],
        'contenido': resultado_reescritura['contenido'],
        'resumen': resumen,
        'puntos_clave': puntos_clave,
        'exitoso': True
    }


# Función de utilidad para verificar que la configuración está lista
def verificar_configuracion():
    """
    Verifica que Gemini está configurado correctamente
    
    Returns:
        bool: True si está configurado, False si no
    """
    if not Config.GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY no configurada")
        return False
    
    try:
        # Prueba simple
        test_response = model.generate_content("Di 'OK'")
        return True
    except Exception as e:
        print(f"❌ ERROR al conectar con Gemini: {e}")
        return False


# Verifico la configuración al importar el módulo
if __name__ != "__main__":
    if not verificar_configuracion():
        print("⚠️  WARNING: Procesador de IA no está configurado correctamente")