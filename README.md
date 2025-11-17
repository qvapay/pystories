# pystories

API REST para publicar historias (stories) en Telegram de forma automatizada usando Telethon y FastAPI.

## Descripción

Este proyecto proporciona una API REST que permite publicar historias en Telegram mediante una interfaz HTTP. Utiliza Telethon para interactuar con la API de Telegram y FastAPI como framework web para exponer los endpoints.

## Características

- 📸 Publicación de historias en Telegram desde una URL de imagen
- 🎨 Soporte para agregar texto/caption a las historias
- 🔐 Autenticación mediante API ID y API Hash de Telegram
- 🚀 API REST simple y fácil de usar
- 💚 Endpoint de health check para monitoreo

## Requisitos

- Python 3.7+
- API ID y API Hash de Telegram (obtenerlos en [my.telegram.org](https://my.telegram.org))
- Cuenta de Telegram con permisos para publicar historias

## Instalación

1. Clona el repositorio:
```bash
git clone <repository-url>
cd tg-stories
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` con tus credenciales:
```
API_ID=tu_api_id
API_HASH=tu_api_hash
```

## Uso

1. Inicia el servidor:
```bash
uvicorn server:app --reload
```

2. Publica una historia mediante POST a `/story`:
```bash
curl -X POST http://localhost:8000/story \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrl": "https://ejemplo.com/imagen.jpg",
    "caption": "Texto opcional para la historia"
  }'
```

## Endpoints

### POST `/story`
Publica una historia en Telegram.

**Parámetros:**
- `imageUrl` (requerido): URL de la imagen a publicar
- `caption` (opcional): Texto que acompañará la historia

**Respuesta exitosa:**
```json
{
  "ok": true,
  "result": "..."
}
```

### GET `/health`
Verifica el estado del servidor.

**Respuesta:**
```json
{
  "ok": true,
  "status": "running"
}
```

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido
- [Telethon](https://docs.telethon.dev/) - Cliente de Telegram para Python
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Manejo de variables de entorno

## Notas

- La primera vez que ejecutes el servidor, Telegram te pedirá autenticarte mediante código de verificación
- El archivo de sesión se guarda localmente para evitar re-autenticaciones
- Asegúrate de tener los permisos necesarios en tu cuenta de Telegram para publicar historias
