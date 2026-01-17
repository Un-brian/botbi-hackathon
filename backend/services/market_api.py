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
        self.stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX', 'AMD', 'INTC']
        self.crypto_ids = ['bitcoin', 'ethereum', 'binancecoin', 'ripple', 'solana', 'cardano', 'polkadot', 'dogecoin', 'avalanche-2', 'shiba-inu']
        
        # Sistema de Caché en memoria
        self._cache = {
            'stocks': {'data': [], 'timestamp': None},
            'crypto': {'data': [], 'timestamp': None}
        }
        self.cache_duration = timedelta(minutes=10) 

    def _es_cache_valido(self, tipo):
        """Verifico si mis datos guardados siguen frescos"""
        cache = self._cache[tipo]
        if not cache['timestamp']:
            return False
        return datetime.now() - cache['timestamp'] < self.cache_duration

    def obtener_top_stocks(self):
        """Obtengo precios de Acciones usando Yahoo Finance"""
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
        """Obtengo precios de Cripto usando CoinGecko API"""
        if self._es_cache_valido('crypto'):
            logger.info("⚡ Usando caché para Cripto")
            return self._cache['crypto']['data']

        logger.info("🔄 Consultando API de CoinGecko...")
        try:
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
                        'nombre': cid.capitalize(),
                        'simbolo': cid[:3].upper(),
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
        return {
            'stocks': self.obtener_top_stocks(),
            'crypto': self.obtener_top_crypto()
        }