"""
Servidor Principal - Botbi Pulse
Punto de entrada de la aplicación Flask
"""

from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.models import init_db
from backend.routes.news import news_bp

def create_app():
    """
    Factory function para crear la aplicación Flask
    Patrón recomendado para aplicaciones Flask modulares
    """
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(Config)
    
    # Habilitar CORS
    CORS(app)
    
    # Inicializar base de datos
    init_db()
    
    # Registrar blueprints (módulos de rutas)
    app.register_blueprint(news_bp, url_prefix='/api')
    
    # Ruta raíz (health check)
    @app.route('/')
    def index():
        return jsonify({
            'service': 'Botbi Pulse API',
            'version': '1.0.0',
            'status': 'online',
            'endpoints': {
                'news': '/api/news',
                'status': '/api/status',
                'health': '/api/health'
            }
        }), 200
    
    # Health check
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'ai': 'configured' if Config.GEMINI_API_KEY else 'not configured'
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("🚀 BOTBI PULSE - Sistema Automatizado de Noticias")
    print("=" * 60)
    print(f"📊 Base de datos: {Config.DATABASE_PATH}")
    print(f"🌐 Servidor: http://{Config.HOST}:{Config.PORT}")
    print(f"🤖 IA configurada: {'✅ Sí' if Config.GEMINI_API_KEY else '❌ No'}")
    print("=" * 60)
    print("\n📡 Endpoints disponibles:")
    print("   GET  /api/news          - Obtener noticias")
    print("   POST /api/news          - Crear noticia")
    print("   GET  /api/status        - Estado del sistema")
    print("   GET  /api/health        - Health check")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )