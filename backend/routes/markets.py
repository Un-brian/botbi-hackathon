from flask import Blueprint, jsonify
from backend.services.market_api import MarketData

# Defino el Blueprint para las rutas de mercados
markets_bp = Blueprint('markets', __name__, url_prefix='/api/markets')

# Instancia global del servicio (para mantener el caché vivo en memoria)
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