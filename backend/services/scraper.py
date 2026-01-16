import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# Configuro logs detallados
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        # CONFIGURACIÓN ROBUSTA
        # User-Agent moderno (Chrome en Windows 10)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        # FUENTES ACTUALIZADAS Y VERIFICADAS (Enero 2026)
        self.feeds = {
            'Tecnología': [
                'https://es.wired.com/feed/rss',      
                'https://techcrunch.com/feed/',       
                'https://www.genbeta.com/feed'       
            ],
            'Negocios': [
                'https://www.forbes.com.mx/feed/',   
                'https://expansion.mx/rss/empresas',  
                'http://feeds.bbci.co.uk/news/business/rss.xml' 
            ]
        }

    def _obtener_soup(self, url):
        """Descarga optimizada con manejo de timeouts y parser XML"""
        try:
            # + timeout a 15s para conexiones lentas (como BBC)
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # MEJORA TÉCNICA: Usamos 'xml' (lxml) en lugar de 'html.parser'
            return BeautifulSoup(response.content, 'xml') 
        except Exception as e:
            logger.error(f"❌ Falló conexión a {url}: {str(e)[:100]}...") 
            return None

    def obtener_noticias_por_categoria(self, categoria, limite=5):
        """Lógica de extracción blindada"""
        noticias = []
        urls = self.feeds.get(categoria, [])
        
        for url in urls:
            if len(noticias) >= limite: break
            
            logger.info(f"📡 Escaneando: {url}")
            soup = self._obtener_soup(url)
            if not soup: continue

            #oporte para RSS estándar (<item>) y Atom (<entry>)
            items = soup.find_all(['item', 'entry'], limit=limite)
            
            for item in items:
                if len(noticias) >= limite: break

                try:
                    # Extracción resiliente (intenta varios tags estándar)
                    titulo = item.find('title').text.strip()
                    
                    link = item.find('link')
                    # Manejo de diferencias entre RSS y Atom
                    if link.get('href'):
                        url_nota = link.get('href')
                    else:
                        url_nota = link.text.strip()

                    # Contenido: Priorizamos content:encoded, luego description, luego summary
                    desc = item.find('content:encoded') or item.find('description') or item.find('summary')
                    contenido_raw = desc.text.strip() if desc else "Detalles en la fuente original."
                    
                    # Limpieza básica de HTML en el texto
                    contenido_limpio = BeautifulSoup(contenido_raw, "html.parser").text

                    noticia = {
                        'titulo': titulo,
                        'contenido': contenido_limpio[:600] + "...", # Límite para IA
                        'categoria': categoria,
                        'fecha': datetime.now().isoformat(),
                        'fuente_original': url_nota
                    }
                    noticias.append(noticia)
                    
                except AttributeError:
                    continue # Si falta un campo crítico, saltamos la noticia
                except Exception as e:
                    logger.warning(f"⚠️ Error procesando item en {url}: {e}")
                    continue
        
        return noticias

    def obtener_todas_las_noticias(self):
        """Interfaz pública del servicio"""
        return {
            'Tecnología': self.obtener_noticias_por_categoria('Tecnología'),
            'Negocios': self.obtener_noticias_por_categoria('Negocios')
        }