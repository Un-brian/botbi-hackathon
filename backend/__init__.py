from flask import Flask
from flask_cors import CORS
from backend.models import init_db

def create_app():
    """Factory para crear la aplicación Flask"""
    
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'dev-secret-key-botbi'
    
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # Permitir todo en desarrollo
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
            "expose_headers": ["Content-Range", "X-Content-Range"]
        }
    })
    
    # Inicializar base de datos
    with app.app_context():
        init_db()
    
    # Registrar blueprints
    from backend.routes.news import news_bp
    from backend.routes.markets import markets_bp
    from backend.routes.newsletter import newsletter_bp
    
    app.register_blueprint(news_bp)
    app.register_blueprint(markets_bp)
    app.register_blueprint(newsletter_bp)
    
    # Health check
    @app.route('/api/status')
    def status():
        return {'status': 'ok', 'message': 'BOTBI PULSE API funcionando 🚀'}
    
    return app
