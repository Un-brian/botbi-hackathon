"""
BOTBI PULSE - Sistema de Automatización Optimizado
- Noticias: Cada 1 hora (respetando límite 5 requests/min de Gemini)
- Mercados: Cada 3 minutos
"""

import schedule
import time
from datetime import datetime, timedelta
import sys
import os
import logging


# Configuración de logging para ver qué pasa en el hilo secundario
logging.basicConfig(level=logging.INFO, format='%(asctime)s - SCHEDULER - %(message)s')

# Asegurar path del proyecto 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importaciones (dentro de try/catch por si hay problemas de path al importar desde app.py)
try:
    from backend.services.scraper import obtener_todas_las_noticias
    from backend.services.ai_processor import procesar_noticia_completa
    from backend.models import crear_noticia, get_db_connection
    from backend.services.market_api import MarketData
except ImportError:
    # Fallback si se ejecuta desde root
    from backend.services.scraper import obtener_todas_las_noticias
    from backend.services.ai_processor import procesar_noticia_completa
    from backend.models import crear_noticia, get_db_connection
    from backend.services.market_api import MarketData

def limpiar_noticias_antiguas():
    """Elimina noticias con más de 24 horas de antigüedad"""
    try:
        fecha_limite = (datetime.now() - timedelta(hours=24)).isoformat()
        
        conn = get_db_connection()
        cursor = conn.execute('DELETE FROM noticias WHERE fecha < ?', (fecha_limite,))
        eliminadas = cursor.rowcount
        conn.commit()
        conn.close()
        
        if eliminadas > 0:
            print(f"🗑️  {eliminadas} noticias antiguas eliminadas (anteriores a {fecha_limite[:16]})")
        
    except Exception as e:
        print(f"❌ Error limpiando noticias: {e}")

# TAREAS  ============================================================


def tarea_actualizar_noticias():
    """Tarea de noticias: scraping + IA + guardado en BD"""
    print("\n" + "="*60)
    print(f"📰 TAREA NOTICIAS INICIADA: {datetime.now().strftime('%H:%M:%S')}")
    print("="*60 + "\n")
    
    try:
        print("📡 Obteniendo noticias RSS...")
        resultado = obtener_todas_las_noticias(limite_por_categoria=3)
        total_obtenidas = resultado.get('total', 0)
        
        if total_obtenidas == 0:
            print("⚠️  No hay noticias nuevas.")
            return
        
        print("🤖 Procesando con Gemini AI (Rate Limit Activo)...")
        noticias_guardadas = 0
        
        for categoria in ['Tecnología', 'Negocios']:
            noticias_cat = resultado.get(categoria, [])
            if not noticias_cat: continue
            
            # Procesar 2 por categoría 
            for i, noticia in enumerate(noticias_cat[:2], 1):
                try:
                    procesado = procesar_noticia_completa(
                        noticia['titulo'], noticia['contenido'], categoria
                    )
                    
                    if procesado.get('exitoso'):
                        crear_noticia(
                            titulo=procesado['titulo'],
                            contenido=procesado['contenido'],
                            categoria=categoria,
                            fuente_original=noticia.get('fuente_original', '')
                        )
                        noticias_guardadas += 1
                        print(f"  ✅ [Guardada] {procesado['titulo'][:40]}...")
                    
                    # Rate limit crítico
                    if i < 2: time.sleep(40)
                
                except Exception as e:
                    print(f"  ❌ Error noticia: {e}")
            
            if categoria == 'Tecnología': time.sleep(15) # Pausa entre categorías
        
        print(f"✅ FIN NOTICIAS: {noticias_guardadas} nuevas.")
        limpiar_noticias_antiguas()
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO NOTICIAS: {e}")

def tarea_actualizar_mercados():
    """Tarea de mercados: actualizar caché"""
    try:
        print(f"💹 Actualizando mercados: {datetime.now().strftime('%H:%M:%S')}")
        market = MarketData()
        c = market.obtener_top_crypto()
        s = market.obtener_top_stocks()
        print(f"   -> Criptos: {len(c)} | Stocks: {len(s)}")
    except Exception as e:
        print(f"   -> ❌ Error mercados: {str(e)}")

# FUNCIÓN PRINCIPAL DEL SCHEDULER

def iniciar_scheduler():
    """Función para arrancar el scheduler (llamada desde app.py o __main__)"""
    print("\n" + "="*70)
    print(" 🤖 BOTBI PULSE - SCHEDULER BACKGROUND")
    print("="*70)
    
    # 1. Programar tareas
    schedule.every(1).hours.do(tarea_actualizar_noticias)
    schedule.every(3).minutes.do(tarea_actualizar_mercados)
    #schedule.every().day.at("20:00").do() crear funcion para enviar a todos

    # 2. EJECUCIÓN INMEDIATA (PARA LA DEMO)
    print("🚀 MODO DEMO: Ejecutando tareas iniciales YA...")
    
    # Primero Mercados (Rápido)
    tarea_actualizar_mercados()
    
    # Segundo Noticias (Lento - IA)
    print("⏳ Iniciando carga inicial de noticias (esto tomará unos minutos)...")
    tarea_actualizar_noticias()

    print("\n♾️  Scheduler en bucle (Noticias 1h | Mercados 3m)")
    
    # 3. Loop Infinito
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("🛑 Scheduler detenido.")

if __name__ == '__main__':
    iniciar_scheduler()