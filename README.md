#  IASanic

Servidor puente para la API **Google Gemini**, construido con **Sanic**.  
Permite generar texto, analizar preguntas y crear respuestas RAG de forma centralizada mediante endpoints REST.  

Ideal para montar un **servidor IA local o en red**, integrable con cualquier aplicación o microservicio.

---

##  Características

- Servidor HTTP rápido basado en **Sanic**
- Conexión directa con **Google Generative AI (Gemini)**
- Soporte para **RAG** (retrieval-augmented generation)
- Endpoints para generación, análisis y verificación
- Fácil de desplegar con **Nginx + systemd**
- Compatible con **Python 3.10+**
- Licencia **MIT**

## Instalación Rápida

### Clonar repositorio

```bash
git clone https://github.com/hugomrj/iasanic.git
cd iasanic
```



### Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```


### Instalar dependencias

```bash
pip install -r requirements.txt
```



## Configuración

Crear `app/google_keys.json`:

```json
{
  "GOOGLE_API_KEYS": [
    "tu_api_key_1",
    "tu_api_key_2"
  ]
}
```

## Uso

### Desarrollo
python app/app.py

### Producción
sanic app.app:app --workers=4 --host=0.0.0.0 --port=8000

## Endpoints

### Generación de texto

```bash
curl -X POST http://localhost:8000/generate/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hola, ¿quién eres?"}'
```


### RAG

```bash
curl -X POST http://localhost:8000/generate_rag \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "¿Cuántos días de vacaciones tengo?",
    "context": "Política de vacaciones",
    "datos": "Información adicional"
  }'
```


### Health Check
```bash
curl http://localhost:8000/health
```




### RAG

```bash
curl -X POST http://localhost:8000/generate_rag \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "¿Cuántos días de vacaciones tengo?",
    "context": "Política de vacaciones",
    "datos": "Información adicional"
  }'
```


## Despliegue en Producción

Ver la guía completa en el repositorio para configuración con:
- Nginx
- Systemd
- SSL/TLS

## Licencia

MIT License - ver LICENSE para más detalles.

