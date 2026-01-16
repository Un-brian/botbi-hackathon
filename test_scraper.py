import logging
from backend.services.scraper import NewsScraper
import json

# Configurar logs para ver qué pasa
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_scraping_cycle():
    print("🕷️ INICIANDO PRUEBA DE SCRAPER...")
    
    scraper = NewsScraper()
    
    # 1. Probar obtención de noticias (Tecnología)
    print("\n📡 Probando fuente: Tecnología...")
    noticias_tech = scraper.obtener_noticias_por_categoria('Tecnología', limite=2)
    
    if noticias_tech:
        print(f"✅ Éxito! Se encontraron {len(noticias_tech)} noticias de Tecnología.")
        print(f"   Ejemplo: {noticias_tech[0]['titulo']}")
    else:
        print("❌ Error: No se encontraron noticias de Tecnología.")

    # 2. Probar obtención de noticias (Negocios)
    print("\n📡 Probando fuente: Negocios...")
    noticias_biz = scraper.obtener_noticias_por_categoria('Negocios', limite=2)
    
    if noticias_biz:
        print(f"✅ Éxito! Se encontraron {len(noticias_biz)} noticias de Negocios.")
        print(f"   Ejemplo: {noticias_biz[0]['titulo']}")
    else:
        print("❌ Error: No se encontraron noticias de Negocios.")

    # 3. Resumen final
    print("\n📊 RESUMEN DE LA PRUEBA")
    print("-" * 30)
    total = len(noticias_tech) + len(noticias_biz)
    print(f"Total noticias capturadas: {total}")
    
    if total > 0:
        print("🚀 EL SCRAPER FUNCIONA CORRECTAMENTE")
    else:
        print("⚠️ REVISAR CONEXIÓN O SELECTORES HTML")

if __name__ == "__main__":
    test_scraping_cycle()