"""
Servidor Principal - Botbi Pulse
Punto de entrada: Importa la app factory y lanza el Scheduler.
"""

import threading
from backend import create_app
from backend.config import Config
# Importamos la función de arranque del scheduler
from automation.scheduler import iniciar_scheduler

# Inicializamos la aplicación
app = create_app()

def run_scheduler_background():
    """Wrapper para correr el scheduler en un hilo daemon"""
    try:
        iniciar_scheduler()
    except Exception as e:
        print(f"❌ Error fatal en scheduler thread: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print(" 🚀 BOTBI PULSE - FULL STACK ONLINE")
    print("=" * 60)
    print(f" 📂 Base de datos: {Config.DATABASE_PATH}")
    print(f" 📡 Servidor: http://{Config.HOST}:{Config.PORT}")
    print("=" * 60)

    # AUTOLOADER: Arrancar Scheduler en Hilo Secundario para no usar dos terminales 
    print(" ⚙️  Iniciando motor de automatización (Scheduler)...")
    scheduler_thread = threading.Thread(target=run_scheduler_background)
    scheduler_thread.daemon = True # Se cierra cuando se cierra la app principal
    scheduler_thread.start()
    # -----------------------------------------------------

    print("\n Endpoints Activos:")
    print("   ✅ API & Web Interface")
    print("   ✅ Scheduler Background (Noticias + Mercados)\n")

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        use_reloader=False # Importante False para que no duplique el scheduler en debug
    )