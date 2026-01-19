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
    """
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias
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

# Funciones para NOTICIAS

def crear_noticia(titulo, contenido, categoria, subcategoria=None, fuente_original=None, 
                  simbolo=None, precio=None, cambio_porcentual=None):
    """
    Crea una nueva noticia en la base de datos
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
    conn = get_db_connection()
    noticias = conn.execute('SELECT * FROM noticias ORDER BY fecha DESC').fetchall()
    conn.close()
    return [dict(noticia) for noticia in noticias]

def obtener_noticias_por_categoria(categoria):
    conn = get_db_connection()
    noticias = conn.execute(
        'SELECT * FROM noticias WHERE categoria = ? ORDER BY fecha DESC',
        (categoria,)
    ).fetchall()
    conn.close()
    return [dict(noticia) for noticia in noticias]

def obtener_top_noticias(limite=10):
    conn = get_db_connection()
    noticias = conn.execute(
        'SELECT * FROM noticias ORDER BY fecha DESC LIMIT ?',
        (limite,)
    ).fetchall()
    conn.close()
    return [dict(noticia) for noticia in noticias]

def contar_noticias():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) as total FROM noticias').fetchone()['total']
    conn.close()
    return count


#funciones adicionales =================================================

def crear_suscriptor(email, nombre=None):
    """
    Crea un nuevo suscriptor o REACTIVA uno existente si estaba dado de baja.
    """
    email_limpio = email.lower().strip()
    suscriptor_id = str(uuid.uuid4())
    fecha_actual = datetime.now().isoformat()
    
    conn = get_db_connection()
    
    try:
        # INTENTO 1: Insertar nuevo usuario
        conn.execute('''
            INSERT INTO suscriptores (id, email, nombre, fecha_suscripcion, activo)
            VALUES (?, ?, ?, ?, 1)
        ''', (suscriptor_id, email_limpio, nombre, fecha_actual))
        
        conn.commit()
        conn.close()
        
        return {
            'id': suscriptor_id,
            'email': email_limpio,
            'nombre': nombre,
            'fecha_suscripcion': fecha_actual,
            'activo': True
        }
        
    except sqlite3.IntegrityError:
        # INTENTO 2: El email ya existe. Verificamos si está inactivo para reactivarlo.
        
        # Buscamos el usuario existente
        usuario = conn.execute(
            'SELECT id, activo, nombre FROM suscriptores WHERE email = ?', 
            (email_limpio,)
        ).fetchone()
        
        if usuario:
            if usuario['activo'] == 0:
                # CASO: Usuario existía pero estaba dado de baja -> LO REACTIVAMOS
                conn.execute(
                    'UPDATE suscriptores SET activo = 1, nombre = ? WHERE email = ?',
                    (nombre if nombre else usuario['nombre'], email_limpio)
                )
                conn.commit()
                conn.close()
                
                print(f"♻️ Usuario {email_limpio} reactivado exitosamente.")
                return {
                    'id': usuario['id'],
                    'email': email_limpio,
                    'nombre': nombre if nombre else usuario['nombre'],
                    'activo': True,
                    'mensaje': 'Reactivado'
                }
            else:
                # CASO: Usuario ya existe y ya está activo -> ERROR REAL
                conn.close()
                raise ValueError('Este correo ya se encuentra suscrito y activo.')
        
        conn.close()
        raise ValueError('Error de base de datos al procesar suscripción.')

def obtener_suscriptores_activos():
    conn = get_db_connection()
    suscriptores = conn.execute(
        'SELECT * FROM suscriptores WHERE activo = 1 ORDER BY fecha_suscripcion DESC'
    ).fetchall()
    conn.close()
    return [dict(s) for s in suscriptores]

def desactivar_suscriptor(email):
    """
    Desactiva un suscriptor (Soft Delete: activo = 0)
    """
    conn = get_db_connection()
    cursor = conn.execute(
        'UPDATE suscriptores SET activo = 0 WHERE email = ?',
        (email.lower().strip(),)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    return rows_affected > 0

def contar_suscriptores():
    conn = get_db_connection()
    count = conn.execute(
        'SELECT COUNT(*) as total FROM suscriptores WHERE activo = 1'
    ).fetchone()['total']
    conn.close()
    return count