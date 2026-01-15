"""
Rutas de Noticias - Endpoints para gestionar noticias
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models import (
    crear_noticia, 
    obtener_todas_noticias, 
    obtener_noticias_por_categoria,
    contar_noticias
)
from backend.config import Config

# Crear blueprint (módulo de rutas)
news_bp = Blueprint('news', __name__)

@news_bp.route('/news', methods=['GET'])
def get_news():
    """
    GET /api/news
    Obtiene todas las noticias o filtra por categoría
    
    Query params:
        - categoria (optional): Tecnología, Negocios, Mercados
    
    Response:
        {
            "success": true,
            "count": 15,
            "data": [...]
        }
    """
    try:
        # Verificar si se solicitó filtro por categoría
        categoria = request.args.get('categoria')
        
        if categoria:
            # Validar categoría
            if categoria not in Config.CATEGORIAS_VALIDAS:
                return jsonify({
                    'success': False,
                    'error': f'Categoría inválida. Debe ser: {", ".join(Config.CATEGORIAS_VALIDAS)}'
                }), 400
            
            noticias = obtener_noticias_por_categoria(categoria)
        else:
            noticias = obtener_todas_noticias()
        
        return jsonify({
            'success': True,
            'count': len(noticias),
            'data': noticias
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@news_bp.route('/news', methods=['POST'])
def create_news():
    """
    POST /api/news
    Crea una nueva noticia
    
    Body:
        {
            "titulo": "...",
            "contenido": "...",
            "categoria": "Tecnología",
            "subcategoria": "Acciones" (opcional, solo para Mercados),
            "fuente_original": "https://..." (opcional),
            "simbolo": "AAPL" (opcional, para Mercados),
            "precio": 150.25 (opcional, para Mercados),
            "cambio_porcentual": 2.5 (opcional, para Mercados)
        }
    
    Response:
        {
            "success": true,
            "message": "Noticia creada exitosamente",
            "data": {...}
        }
    """
    try:
        data = request.get_json()
        
        # Validar campos obligatorios
        if not data or not all(k in data for k in ('titulo', 'contenido', 'categoria')):
            return jsonify({
                'success': False,
                'error': 'Faltan campos obligatorios: titulo, contenido, categoria'
            }), 400
        
        # Validar categoría
        if data['categoria'] not in Config.CATEGORIAS_VALIDAS:
            return jsonify({
                'success': False,
                'error': f'Categoría inválida. Debe ser: {", ".join(Config.CATEGORIAS_VALIDAS)}'
            }), 400
        
        # Validar subcategoría si es Mercados
        if data['categoria'] == 'Mercados':
            subcategoria = data.get('subcategoria')
            if subcategoria and subcategoria not in Config.SUBCATEGORIAS_MERCADOS:
                return jsonify({
                    'success': False,
                    'error': f'Subcategoría inválida. Debe ser: {", ".join(Config.SUBCATEGORIAS_MERCADOS)}'
                }), 400
        
        # Crear noticia
        noticia = crear_noticia(
            titulo=data['titulo'],
            contenido=data['contenido'],
            categoria=data['categoria'],
            subcategoria=data.get('subcategoria'),
            fuente_original=data.get('fuente_original'),
            simbolo=data.get('simbolo'),
            precio=data.get('precio'),
            cambio_porcentual=data.get('cambio_porcentual')
        )
        
        return jsonify({
            'success': True,
            'message': 'Noticia creada exitosamente',
            'data': noticia
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@news_bp.route('/status', methods=['GET'])
def get_status():
    """
    GET /api/status
    Devuelve el estado del sistema (para IoT)
    
    Response:
        {
            "alert_level": "normal" | "high",
            "news_count": 15,
            "timestamp": "2025-01-14T10:30:00"
        }
    """
    try:
        count = contar_noticias()
        alert_level = "high" if count > 5 else "normal"
        
        return jsonify({
            'alert_level': alert_level,
            'news_count': count,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500