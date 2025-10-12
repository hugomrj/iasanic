# IA Sanic

Servidor puente para IA con Sanic y Google Generative AI

## Características

- Alto rendimiento con Sanic
- Múltiples endpoints para IA
- CORS habilitado
- Gestión de múltiples API keys
- Endpoints de monitoreo
- Soporte para RAG
- Listo para producción

## Instalación Rápida

# Clonar repositorio
git clone https://github.com/hugomrj/iasanic.git
cd iasanic

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

## Configuración

Crear app/google_keys.json:

{
  "GOOGLE_API_KEYS": [
    "tu_api_key_1",
    "tu_api_key_2"
  ]
}

## Uso

### Desarrollo
python app/app.py

### Producción
sanic app.app:app --workers=4 --host=0.0.0.0 --port=8000

## Endpoints

### Generación de texto
curl -X POST http://localhost:8000/generate/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hola, ¿quién eres?"}'

### RAG
curl -X POST http://localhost:8000/generate_rag \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "¿Cuántos días de vacaciones tengo?",
    "context": "Política de vacaciones",
    "datos": "Información adicional"
  }'

### Health Check
curl http://localhost:8000/health

## Estructura del Proyecto

iasanic/
├── app/
│   ├── app.py              # Aplicación principal
│   ├── config.py           # Configuración
│   ├── services.py         # Servicios IA
│   ├── normalizador_funcion.py
│   └── google_keys.json    # API keys
├── requirements.txt
└── README.md

## Despliegue en Producción

Ver la guía completa en el repositorio para configuración con:
- Nginx
- Systemd
- SSL/TLS

## Licencia

MIT License - ver LICENSE para más detalles.

## Autor

Hugo Romero
