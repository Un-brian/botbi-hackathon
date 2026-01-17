from flask import Blueprint, jsonify
from backend.services.market_api import MarketData

# ⚠️ ELIMINÉ LAS IMPORTACIONES QUE CAUSABAN EL ERROR (obtener_top_...)

# Defino el Blueprint para las rutas de mercados
markets_bp = Blueprint('markets', __name__, url_prefix='/api/markets')

# Instancia global del servicio
market_service = MarketData()

@markets_bp.route('/stocks', methods=['GET'])
def get_stocks():
    """Endpoint para Top 10 Acciones"""
    data = market_service.obtener_top_stocks()
    return jsonify(data)

@markets_bp.route('/crypto', methods=['GET'])
def get_crypto():
    """Endpoint para Top 10 Criptomonedas"""
    data = market_service.obtener_top_crypto()
    return jsonify(data)

@markets_bp.route('/all', methods=['GET'])
def get_all_markets():
    """Resumen completo para el Dashboard"""
    data = market_service.obtener_todo_el_mercado()
    return jsonify(data)

@markets_bp.route('/ticker', methods=['GET'])
def get_ticker():
    """Datos simplificados para el ticker animado"""
    try:
        # CORRECCIÓN: Usamos la instancia de la clase, no una función suelta
        data = market_service.obtener_top_crypto()
        
        # Filtramos las primeras 5 y adaptamos las claves para el frontend
        ticker_data = []
        for item in data[:5]:
            ticker_data.append({
                'symbol': item['simbolo'], # Mapeo 'simbolo' -> 'symbol'
                'name': item['nombre'],
                'price': item['precio'],
                'change_percent': item['cambio_porcentual']
            })
            
        return jsonify(ticker_data), 200
        
    except Exception as e:
        print(f"⚠️ Error en Ticker: {e}")
        # Fallback por si falla la API
        return jsonify([
            {'symbol': 'BTC', 'price': 43500, 'change_percent': 2.5},
            {'symbol': 'ETH', 'price': 2320, 'change_percent': -1.2}
        ]), 200