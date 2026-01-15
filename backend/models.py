"""
Modelos de Base de Datos - Botbi Pulse
Define la estructura de las tablas y funciones para interactuar con SQLite
"""

import sqlite3
from datetime import datetime
import uuid
from backend.config import Config

def get_db_connection():
    """
    Establece conexión con la base de datos SQLite
    
    Returns:
        sqlite3.Connection: Conexión a la base de datos
    """
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias
    Se ejecuta automáticamente al iniciar la aplicación
    """
    conn = get_db_connection()
    
    # Tabla de Noticias
    conn.execute('''
        CREATE TABLE IF NOT EXISTS noticias (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            categoria TEXT NOT NULL,
            subcategoria TEXT,
            fecha TEXT NOT NULL,
            fuente_original TEXT,
            procesado_ia INTEGER DEFAULT 1,
            simbolo TEXT,
            precio REAL,
            cambio_porcentual REAL
        )
    ''')
    
    # Tabla de Suscriptores (para newsletter)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS suscriptores (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            nombre TEXT,
            fecha_suscripcion TEXT NOT NULL,
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Tabla de Newsletters enviados (historial)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS newsletters_enviados (
            id TEXT PRIMARY KEY,
            fecha_envio TEXT NOT NULL,
            destinatarios INTEGER NOT NULL,
            noticias_incluidas TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Base de datos inicializada correctamente")

# Funciones auxiliares para la tabla de noticias

def crear_noticia(titulo, contenido, categoria, subcategoria=None, fuente_original=None, 
                  simbolo=None, precio=None, cambio_porcentual=None):
    """
    Crea una nueva noticia en la base de datos
    
    Args:
        titulo (str): Título de la noticia
        contenido (str): Contenido completo
        categoria (str): Tecnología, Negocios o Mercados
        subcategoria (str, optional): Para Mercados: Acciones o Criptomonedas
        fuente_original (str, optional): URL de la fuente original
        simbolo (str, optional): Símbolo de la acción/cripto (ej: AAPL, BTC)
        precio (float, optional): Precio actual
        cambio_porcentual (float, optional): Cambio porcentual
    
    Returns:
        dict: Noticia creada con su ID
    """
    noticia_id = str(uuid.uuid4())
    fecha_actual = datetime.now().isoformat()
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO noticias 
        (id, titulo, contenido, categoria, subcategoria, fecha, fuente_original, 
         simbolo, precio, cambio_porcentual)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (noticia_id, titulo, contenido, categoria, subcategoria, fecha_actual, 
          fuente_original, simbolo, precio, cambio_porcentual))
    
    conn.commit()
    conn.close()
    
    return {
        'id': noticia_id,
        'titulo': titulo,
        'contenido': contenido,
        'categoria': categoria,
        'subcategoria': subcategoria,
        'fecha': fecha_actual,
        'fuente_original': fuente_original,
        'simbolo': simbolo,
        'precio': precio,
        'cambio_porcentual': cambio_porcentual
    }

def obtener_todas_noticias():
    """
    Obtiene todas las noticias ordenadas por fecha descendente
    
    Returns:
        list: Lista de noticias
    """
    conn = get_db_connection()
    noticias = conn.execute(
        'SELECT * FROM noticias ORDER BY fecha DESC'
    ).fetchall()
    conn.close()
    
    return [dict(noticia) for noticia in noticias]

def obtener_noticias_por_categoria(categoria):
    """
    Obtiene noticias filtradas por categoría
    
    Args:
        categoria (str): Tecnología, Negocios o Mercados
    
    Returns:
        list: Lista de noticias de esa categoría
    """
    conn = get_db_connection()
    noticias = conn.execute(
        'SELECT * FROM noticias WHERE categoria = ? ORDER BY fecha DESC',
        (categoria,)
    ).fetchall()
    conn.close()
    
    return [dict(noticia) for noticia in noticias]

def obtener_top_noticias(limite=10):
    """
    Obtiene las noticias más recientes (para newsletter)
    
    Args:
        limite (int): Número de noticias a retornar
    
    Returns:
        list: Top N noticias más recientes
    """
    conn = get_db_connection()
    noticias = conn.execute(
        'SELECT * FROM noticias ORDER BY fecha DESC LIMIT ?',
        (limite,)
    ).fetchall()
    conn.close()
    
    return [dict(noticia) for noticia in noticias]

def contar_noticias():
    """
    Cuenta el total de noticias en la base de datos
    
    Returns:
        int: Número total de noticias
    """
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) as total FROM noticias').fetchone()['total']
    conn.close()
    
    return count