from flask import Blueprint, jsonify
from backend.services.market_api import MarketData

markets_bp = Blueprint('markets', __name__, url_prefix='/api/markets')

# Instancia global del servicio
market_service = MarketData()

@markets_bp.route('/stocks', methods=['GET'])
def get_stocks():
    """GET /api/markets/stocks - Top 10 Acciones"""
    data = market_service.obtener_top_stocks()
    return jsonify(data), 200

@markets_bp.route('/crypto', methods=['GET'])
def get_crypto():
    """GET /api/markets/crypto - Top 10 Criptomonedas"""
    data = market_service.obtener_top_crypto()
    return jsonify(data), 200

@markets_bp.route('/all', methods=['GET'])
def get_all_markets():
    """GET /api/markets/all - Resumen completo Dashboard"""
    data = market_service.obtener_todo_el_mercado()
    return jsonify(data), 200

@markets_bp.route('/ticker', methods=['GET'])
def get_ticker():
    """GET /api/markets/ticker - Datos para ticker animado"""
    try:

        data = market_service.obtener_top_crypto()
        return jsonify(data[:5]), 200
        
    except Exception as e:
        print(f"⚠️ Error en Ticker: {e}")
      
        return jsonify([
            {
                'nombre': 'Bitcoin',
                'simbolo': 'BTC',
                'precio': 43500.0,
                'cambio_porcentual': 2.5,
                'tipo': 'crypto'
            },
            {
                'nombre': 'Ethereum',
                'simbolo': 'ETH',
                'precio': 2320.0,
                'cambio_porcentual': -1.2,
                'tipo': 'crypto'
            }
        ]), 200