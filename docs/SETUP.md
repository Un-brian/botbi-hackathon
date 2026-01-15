# 📖 Guía de Instalación - Botbi Pulse

## Requisitos Previos

- Python 3.10 o superior
- Git instalado
- Cuenta de Gmail (para newsletter)
- API Key de Google Gemini

## Paso a Paso

### 1. Obtener API Key de Google Gemini

1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Iniciar sesión con cuenta Google
3. Click en "Create API Key"
4. Copiar la clave generada

### 2. Configurar Variables de Entorno
```bash
# Copiar el template
cp .env.example .env

# Editar con tus datos
notepad .env
```

Agregar tus claves:
```env
GEMINI_API_KEY=TU_CLAVE_AQUI
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=contraseña_de_aplicacion_aqui
```

**Nota**: Para Gmail, usa una "Contraseña de Aplicación", no tu contraseña normal.

### 3. Instalación
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Verificar Instalación
```bash
python -c "import flask; import google.generativeai; print('✅ Todo OK')"
```

### 5. Primera Ejecución
```bash
python backend/app.py
```

Deberías ver:
```
🚀 Iniciando Botbi Pulse Backend...
✅ Base de datos inicializada
 * Running on http://0.0.0.0:5000
```

## Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: Puerto 5000 ocupado
Edita `backend/config.py` y cambia el puerto.

### Error: API Key inválida
Verifica que copiaste correctamente la clave en `.env`