from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import uuid
import os

app = Flask(__name__)
CORS(app)  

# Conf base de datos
DATABASE = 'botbi_pulse.db'

def get_db_connection():
    """Establece conexión con la base de datos SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

def init_db():
    """Inicializa la base de datos con la tabla de noticias"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS noticias (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            categoria TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")


init_db()


# ENDPOINTS DE LA API ==========


@app.route('/api/news', methods=['GET'])
def get_news():
    """
    GET /api/news
    Devuelve todas las noticias almacenadas en formato JSON
    """
    try:
        conn = get_db_connection()
        noticias = conn.execute('SELECT * FROM noticias ORDER BY fecha DESC').fetchall()
        conn.close()
        
        # Convertir a lista de diccionarios
        noticias_list = []
        for noticia in noticias:
            noticias_list.append({
                'id': noticia['id'],
                'titulo': noticia['titulo'],
                'contenido': noticia['contenido'],
                'categoria': noticia['categoria'],
                'fecha': noticia['fecha']
            })
        
        return jsonify({
            'success': True,
            'count': len(noticias_list),
            'data': noticias_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news', methods=['POST'])
def create_news():
    """
    POST /api/news
    Recibe una noticia nueva y la guarda en la base de datos
    Body esperado: {titulo, contenido, categoria}
    """
    try:
        data = request.get_json()
        
        # Validar datos obligatorios
        if not data or not all(k in data for k in ('titulo', 'contenido', 'categoria')):
            return jsonify({
                'success': False,
                'error': 'Faltan campos obligatorios: titulo, contenido, categoria'
            }), 400
        
        # Validar categoría
        categorias_validas = ['Tecnología', 'Negocios', 'Cripto']
        if data['categoria'] not in categorias_validas:
            return jsonify({
                'success': False,
                'error': f'Categoría inválida. Debe ser una de: {", ".join(categorias_validas)}'
            }), 400
        
        # Generar ID único (UUID)
        noticia_id = str(uuid.uuid4())
        
        # Fecha actual en formato ISO
        fecha_actual = datetime.now().isoformat()
        
        # Insertar en la base de datos
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO noticias (id, titulo, contenido, categoria, fecha)
            VALUES (?, ?, ?, ?, ?)
        ''', (noticia_id, data['titulo'], data['contenido'], data['categoria'], fecha_actual))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Noticia creada exitosamente',
            'data': {
                'id': noticia_id,
                'titulo': data['titulo'],
                'contenido': data['contenido'],
                'categoria': data['categoria'],
                'fecha': fecha_actual
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    GET /api/status
    Devuelve el estado del sistema para el dispositivo IoT
    Lógica: Si hay más de 5 noticias, nivel "high", sino "normal"
    """
    try:
        conn = get_db_connection()
        count = conn.execute('SELECT COUNT(*) as total FROM noticias').fetchone()['total']
        conn.close()
        
        # Lógica de alerta simple
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

# Endpoint adicional para health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check básico para verificar que el servidor está corriendo"""
    return jsonify({
        'status': 'online',
        'service': 'Botbi Pulse API',
        'version': '1.0.0'
    }), 200

# PUNTO DE ENTRADA ===========================


if __name__ == '__main__':
    print(" Iniciando Botbi Pulse Backend...")
    print(f" Base de datos: {DATABASE}")
    print(" Servidor corriendo en http://localhost:5000")
    print("\n Endpoints disponibles:")
    print("   GET  /api/news   - Obtener todas las noticias")
    print("   POST /api/news   - Crear nueva noticia")
    print("   GET  /api/status - Estado del sistema (para IoT)")
    print("   GET  /api/health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)