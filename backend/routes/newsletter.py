"""
Routes de Newsletter - Gestión de suscripciones y Envío Inmediato
"""
import smtplib
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.config import Config

from flask import Blueprint, request, jsonify
from backend.models import (
    crear_suscriptor,
    desactivar_suscriptor,
    obtener_top_noticias
)

newsletter_bp = Blueprint('newsletter', __name__, url_prefix='/api/newsletter')

# --- TEMPLATE DE EMAIL

def generar_html_newsletter(noticias, es_preview=False):
    """Genera el HTML del newsletter con estilo Dark/Cyberpunk"""
    header_text = "VISTA PREVIA" if es_preview else "Tu Resumen Inteligente"
    fecha_hoy = time.strftime("%d/%m/%Y")
    
    # Estilos CSS inline para compatibilidad con emails
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Helvetica', 'Arial', sans-serif; background-color: #000000; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: #111827; overflow: hidden; }}
            .header {{ background-color: #000000; padding: 30px 20px; border-bottom: 2px solid #00ff88; text-align: center; }}
            .brand {{ color: #ffffff; font-size: 24px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }}
            .brand span {{ color: #00ff88; }}
            .date {{ color: #6b7280; font-size: 12px; margin-top: 5px; font-family: monospace; }}
            .content {{ padding: 20px; }}
            .intro {{ color: #d1d5db; font-size: 14px; margin-bottom: 25px; text-align: center; line-height: 1.5; }}
            
            /* Tarjeta de Noticia */
            .card {{ background-color: #1f2937; border-radius: 8px; padding: 20px; margin-bottom: 20px; border: 1px solid #374151; }}
            .tag {{ display: inline-block; background-color: rgba(0, 255, 136, 0.1); color: #00ff88; font-size: 10px; font-weight: bold; padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(0, 255, 136, 0.3); margin-bottom: 10px; text-transform: uppercase; }}
            .title {{ color: #ffffff; font-size: 18px; font-weight: bold; margin: 0 0 10px 0; line-height: 1.3; }}
            .excerpt {{ color: #9ca3af; font-size: 14px; line-height: 1.6; margin-bottom: 15px; }}
            .btn-link {{ display: inline-block; color: #00ff88; font-size: 13px; font-weight: bold; text-decoration: none; }}
            
            .footer {{ background-color: #000000; padding: 30px 20px; text-align: center; border-top: 1px solid #374151; }}
            .footer p {{ color: #4b5563; font-size: 12px; margin: 5px 0; }}
            .unsubscribe {{ color: #ef4444; text-decoration: none; font-size: 11px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="brand">BOTBI <span>PULSE</span></div>
                <div class="date">REPORTE DIARIO | {fecha_hoy}</div>
            </div>
            
            <div class="content">
                <p class="intro">
                    Hola. Aquí tienes las {len(noticias)} noticias financieras más relevantes detectadas por nuestra IA en las últimas horas.
                </p>
    """
    
    if not noticias:
        html += """<div class="card"><p style="color:white; text-align:center;">El sistema está escaneando los mercados. Espera al próximo ciclo.</p></div>"""
    else:
        for noticia in noticias:
            # Lógica de recorte para "Resumen"
            contenido_full = noticia.get('contenido', '')
            # Tomamos los primeros 180 caracteres y añadimos 
            resumen = contenido_full[:180].rsplit(' ', 1)[0] + "..." if len(contenido_full) > 180 else contenido_full
            
            categoria = noticia.get('categoria', 'General').upper()
            titulo = noticia.get('titulo', 'Sin título')
            
            # Usamos localhost 
            link = "http://localhost:5000" 
            
            html += f"""
                <div class="card">
                    <span class="tag">{categoria}</span>
                    <h3 class="title">{titulo}</h3>
                    <p class="excerpt">{resumen}</p>
                    <a href="{link}" class="btn-link">LEER ANÁLISIS COMPLETO &rarr;</a>
                </div>
            """
    
    html += """
            </div>
            
            <div class="footer">
                <p>Potenciado por Gemini AI & Python</p>
                <p>BotBi Pulse - Hackathon 2026</p>
                <br>
                <p>¿Deseas dejar de recibir estos reportes?</p>
                <a href="#" style="color: #6b7280; font-size: 11px;">Entra a la plataforma para desuscribirte</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def enviar_email_newsletter(destinatario, html_content):
    """Envía un email con el newsletter usando SMTP"""
    try:
        if not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            print("⚠️  Credenciales SMTP faltantes. No se envió el correo.")
            return False
        
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = '⚡ BotBi Pulse: Tu Resumen Financiero'
        mensaje['From'] = f"BOTBI PULSE <{Config.EMAIL_USER}>"
        mensaje['To'] = destinatario
        mensaje.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(mensaje)
        
        print(f"📧 Email enviado a {destinatario}")
        return True
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

# --- RUTAS ---

@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """POST /api/newsletter/subscribe - Suscribe y envía email al instante"""
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'error': 'Email es requerido'}), 400
        
        email = data.get('email', '').strip()
        nombre = data.get('nombre', '')
        
        # Validación básica
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({'error': 'Formato de email inválido'}), 400
        
        try:
            # 1. Crear o Reactivar suscriptor en BD
            resultado = crear_suscriptor(email, nombre)
            
            # 2. Obtener noticias y enviar email
            print(f"⚡ Procesando envío para: {email}...")
            noticias = obtener_top_noticias(limite=10) # Top 10 para el email
            html_content = generar_html_newsletter(noticias)
            enviar_email_newsletter(email, html_content)
            
            return jsonify({
                'success': True,
                'message': 'Suscripción exitosa',
                'data': resultado
            }), 201
            
        except ValueError as e:
            # Conflicto real (ya existe y está activo)
            return jsonify({'success': False, 'error': str(e)}), 409
        
    except Exception as e:
        print(f"❌ Error en subscribe: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@newsletter_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """POST /api/newsletter/unsubscribe"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        if desactivar_suscriptor(email):
            return jsonify({'success': True, 'message': 'Te has desuscrito correctamente.'})
        return jsonify({'success': False, 'error': 'Email no encontrado en suscriptores activos'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500