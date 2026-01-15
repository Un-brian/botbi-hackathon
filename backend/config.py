"""
Configuración centralizada del proyecto Botbi Pulse
Maneja variables de entorno y configuraciones globales
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Base de Datos
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/botbi_pulse.db')
    
    # Google Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    # Email (para newsletter)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    # Categorías válidas
    CATEGORIAS_VALIDAS = ['Tecnología', 'Negocios', 'Mercados']
    
    # Subcategorías de Mercados
    SUBCATEGORIAS_MERCADOS = ['Acciones', 'Criptomonedas']
    
    # APIs de Mercados
    ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', '')
    COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
    
    # Newsletter
    NEWSLETTER_TOP_COUNT = 10  # Número de noticias en el newsletter
    
    @staticmethod
    def validate():
        """Valida que las configuraciones críticas estén presentes"""
        if not Config.GEMINI_API_KEY:
            print("⚠️  WARNING: GEMINI_API_KEY no configurada")
        
        if not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            print("⚠️  WARNING: Credenciales de email no configuradas")
        
        return True

# Validar configuración al importar
Config.validate()