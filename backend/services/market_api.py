
import yfinance as yf
import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketData:
    def __init__(self):
     
        # Las obtendremos dinámicamente de CoinGecko
        
        # Acciones siguen igual (Yahoo Finance top 10)
        self.stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 
                              'TSLA', 'META', 'NFLX', 'AMD', 'INTC']
        
        # Sistema de Caché
        self._cache = {
            'stocks': {'data': [], 'timestamp': None},
            'crypto': {'data': [], 'timestamp': None}
        }
        self.cache_duration = timedelta(minutes=3)

    def _es_cache_valido(self, tipo):
        """Verificar si caché sigue fresco"""
        cache = self._cache[tipo]
        if not cache['timestamp']:
            return False
        return datetime.now() - cache['timestamp'] < self.cache_duration

    def obtener_top_stocks(self):
        """Obtener precios de Acciones usando Yahoo Finance"""
        if self._es_cache_valido('stocks'):
            logger.info("⚡ Usando caché para Stocks")
            return self._cache['stocks']['data']

        logger.info("🔄 Descargando datos frescos de Yahoo Finance...")
        data = []
        try:
            tickers = yf.Tickers(' '.join(self.stock_symbols))
            for symbol in self.stock_symbols:
                info = tickers.tickers[symbol].info
                stock = {
                    'nombre': info.get('shortName', symbol),
                    'simbolo': symbol,
                    'precio': info.get('currentPrice', 0.0),
                    'cambio_porcentual': info.get('regularMarketChangePercent', 0.0),
                    'tipo': 'stock'
                }
                data.append(stock)
            
            self._cache['stocks'] = {'data': data, 'timestamp': datetime.now()}
            return data

        except Exception as e:
            logger.error(f"❌ Error obteniendo Stocks: {e}")
            return self._cache['stocks']['data']

    def obtener_top_crypto(self):
        """
        ✅ NUEVO: Obtener TOP 10 dinámico desde CoinGecko
        Ya no usamos lista hardcodeada
        """
        if self._es_cache_valido('crypto'):
            logger.info("⚡ Usando caché para Cripto")
            return self._cache['crypto']['data']

        logger.info("🔄 Consultando Top 10 de CoinGecko...")
        try:
            #  ENDPOINT CORRECTO: markets con ordenamiento por market_cap
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',  # Ordenar por capitalización
                'per_page': 10,              # Top 10
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            
            data = []
            for coin in json_data:
                crypto = {
                    'nombre': coin.get('name', 'Unknown'),           # "Bitcoin"
                    'simbolo': coin.get('symbol', '').upper(),       # "BTC"
                    'precio': coin.get('current_price', 0.0),
                    'cambio_porcentual': coin.get('price_change_percentage_24h', 0.0),
                    'tipo': 'crypto',
                    'market_cap': coin.get('market_cap', 0),         # Extra info
                    'rank': coin.get('market_cap_rank', 0)           # Ranking
                }
                data.append(crypto)
            
            self._cache['crypto'] = {'data': data, 'timestamp': datetime.now()}
            logger.info(f"✅ Top 10 obtenido: {[c['simbolo'] for c in data]}")
            
            return data

        except Exception as e:
            logger.error(f"❌ Error en CoinGecko: {e}")
            # Fallback: devolver caché viejo o lista vacía
            return self._cache['crypto']['data'] if self._cache['crypto']['data'] else []

    def obtener_todo_el_mercado(self):
        return {
            'stocks': self.obtener_top_stocks(),
            'crypto': self.obtener_top_crypto()
        }