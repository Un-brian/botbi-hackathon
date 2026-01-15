# 📡 Documentación de API - Botbi Pulse

Base URL: `http://localhost:5000/api`

## Endpoints de Noticias

### GET /api/news
Obtiene todas las noticias publicadas.

**Response:**
```json
{
  "success": true,
  "count": 15,
  "data": [...]
}
```

### POST /api/news
Crea una nueva noticia.

**Request Body:**
```json
{
  "titulo": "...",
  "contenido": "...",
  "categoria": "Tecnología"
}
```