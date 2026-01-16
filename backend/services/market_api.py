import yfinance as yf
import requests
import logging
from datetime import datetime, timedelta

# Configuro logs para monitorear mis APIs financieras
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketData:
    def __init__(self):
        # Defino mis símbolos objetivo para el "Top 10"
        # Estos son los tickers reales de Yahoo Finance
        self.stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX', 'AMD', 'INTC']
        
        # Para Cripto uso los IDs de CoinGecko
        self.crypto_ids = ['bitcoin', 'ethereum', 'binancecoin', 'ripple', 'solana', 'cardano', 'polkadot', 'dogecoin', 'avalanche-2', 'shiba-inu']
        
        # Sistema de Caché en memoria (Hackathon Survival)
        # Guardo los datos aquí para no saturar las APIs externas
        self._cache = {
            'stocks': {'data': [], 'timestamp': None},
            'crypto': {'data': [], 'timestamp': None}
        }
        self.cache_duration = timedelta(minutes=10) # Actualizo cada 10 min

    def _es_cache_valido(self, tipo):
        """Verifico si mis datos guardados siguen frescos"""
        cache = self._cache[tipo]
        if not cache['timestamp']:
            return False
        
        ahora = datetime.now()
        # Si pasó menos de 10 min, el caché sirve
        return ahora - cache['timestamp'] < self.cache_duration

    def obtener_top_stocks(self):
        """Obtengo precios de Acciones usando Yahoo Finance"""
        # 1. Intento usar caché primero
        if self._es_cache_valido('stocks'):
            logger.info("⚡ Usando caché para Stocks")
            return self._cache['stocks']['data']

        logger.info("🔄 Descargando datos frescos de Yahoo Finance...")
        data = []
        try:
            # Descarga masiva (es más rápido que uno por uno)
            tickers = yf.Tickers(' '.join(self.stock_symbols))
            
            for symbol in self.stock_symbols:
                # Extraigo la info cruda
                info = tickers.tickers[symbol].info
                
                # Proceso y limpio el dato
                stock = {
                    'nombre': info.get('shortName', symbol),
                    'simbolo': symbol,
                    'precio': info.get('currentPrice', 0.0),
                    'cambio_porcentual': info.get('regularMarketChangePercent', 0.0),
                    'tipo': 'stock'
                }
                data.append(stock)
            
            # Guardo en caché para la próxima
            self._cache['stocks'] = {'data': data, 'timestamp': datetime.now()}
            return data

        except Exception as e:
            logger.error(f"❌ Error obteniendo Stocks: {e}")
            # Retorno caché viejo si existe, o lista vacía para no romper el frontend
            return self._cache['stocks']['data']

    def obtener_top_crypto(self):
        """Obtengo precios de Cripto usando CoinGecko API"""
        # 1. Caché check
        if self._es_cache_valido('crypto'):
            logger.info("⚡ Usando caché para Cripto")
            return self._cache['crypto']['data']

        logger.info("🔄 Consultando API de CoinGecko...")
        try:
            # URL oficial gratuita de CoinGecko
            ids_str = ','.join(self.crypto_ids)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            
            data = []
            for cid in self.crypto_ids:
                if cid in json_data:
                    item = json_data[cid]
                    crypto = {
                        'nombre': cid.capitalize(), # CoinGecko devuelve id minúscula
                        'simbolo': cid[:3].upper(), # Aproximación (BTC, ETH...)
                        'precio': item.get('usd', 0.0),
                        'cambio_porcentual': item.get('usd_24h_change', 0.0),
                        'tipo': 'crypto'
                    }
                    data.append(crypto)
            
            self._cache['crypto'] = {'data': data, 'timestamp': datetime.now()}
            return data

        except Exception as e:
            logger.error(f"❌ Error en CoinGecko: {e}")
            return self._cache['crypto']['data']

    def obtener_todo_el_mercado(self):
        """Función helper para el Dashboard"""
        return {
            'stocks': self.obtener_top_stocks(),
            'crypto': self.obtener_top_crypto()
        }