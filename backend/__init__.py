from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar la base de datos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # 1. Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
    
    # Configuración de ruta de Base de Datos
    basedir = os.path.abspath(os.path.dirname(__file__))
    # La base de datos se guardará en la carpeta 'backend'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'botbi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 2. Inicializar extensiones
    CORS(app)      # Permite que el Frontend hable con el Backend
    db.init_app(app) # Conecta la base de datos

    # 3. Registrar Rutas (Blueprints)
    # Aquí importamos y activamos los "mapas" de tu API
    
    # Rutas de Noticias
    from backend.routes.news import news_bp
    app.register_blueprint(news_bp)
    
    # Rutas de Mercados (LO NUEVO)
    from backend.routes.markets import markets_bp
    app.register_blueprint(markets_bp)

    # 4. Crear tablas de base de datos si no existen
    with app.app_context():
        db.create_all()

    return app

