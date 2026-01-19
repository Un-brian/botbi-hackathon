# 🤖 Botbi Pulse - Sistema Automatizado de Noticias

> Proyecto para Hackathon Botbi 2026 - Landing Page Inteligente y Newsletter Automatizado

## 📋 Descripción

Sistema completo de gestión de noticias que automatiza el ciclo desde la obtención hasta la entrega:

1. **Obtención** - Web scraping de fuentes confiables
2. **Procesamiento** - Reescritura con IA (Google Gemini)
3. **Publicación** - Landing page segmentada por categorías
4. **Newsletter** - Envío automático de las 10 noticias más relevantes

## 🏗️ Tecnologías

- **Backend**: Python 3.10+ | Flask | SQLite
- **Frontend**: HTML5 | TailwindCSS | JavaScript Vanilla
- **IA**: Google Gemini API
- **Automatización**: Schedule
- **Web Scraping**: BeautifulSoup4


## 📁 Estructura del Proyecto

```text
BotBi/
├── automation/           # Automatización
│   └── scheduler.py      # Orquestador de tareas (Daemon)
├── backend/              # Núcleo del Servidor
│   ├── routes/           # Endpoints API (markets.py, news.py, newsletter.py)
│   ├── services/         # Lógica de Negocio (ai_processor.py, scraper.py, market_api.py)
│   ├── __init__.py       # Inicialización de la App (Factory)
│   ├── config.py         # Configuración del entorno
│   └── models.py         # Modelos de Base de Datos
├── data/                 # Almacenamiento local
│   ├── .gitkeep          # Mantiene la carpeta en git
│   └── botbi_pulse.db    # Base de datos SQLite
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Archivos ignorados por git
├── app.py                # Punto de entrada principal
├── index.html            # Frontend (Landing Page & Dashboard)
├── poblar_bd.py          # Script para generar datos de prueba
├── Readme.md             # Documentación del proyecto
├── requirements.txt      # Dependencias y librerías
└── test_*.py             # Pruebas unitarias (ai, gemini, models, scraper)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/botbi-pulse-hackathon.git
cd botbi-pulse-hackathon
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus API keys
```

### 5. Iniciar el servidor
```bash
python backend/app.py
```

## 🎯 Características

- ✅ UUID único para cada noticia
- ✅ Categorías: Tecnología, Negocios, Mercados
- ✅ Top 10 Acciones y Criptomonedas
- ✅ Reescritura automática con IA
- ✅ Newsletter responsivo
- ✅ Automatización completa

## 📡 API Endpoints


- `GET /api/news` - Obtener noticias
- `POST /api/news` - Crear noticia
- `GET /api/markets/stocks` - Top 10 acciones
- `GET /api/markets/crypto` - Top 10 criptos
- `POST /api/newsletter/subscribe` - Suscribirse
- `POST /api/newsletter/send` - Enviar newsletter

## 👥 Autor

Desarrollado por Brian FLores para Hackathon Botbi 2026

## 📅 Timeline

- **Inicio**: 14 de Enero 2026
- **Entrega**: 18 de Enero 2026, 11:59 PM