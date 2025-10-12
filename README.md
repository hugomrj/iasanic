#  IASanic

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Status](https://img.shields.io/badge/status-stable-success.svg)]()



Servidor **gateway para la API Google Gemini**, construido con **Sanic**.  
Centraliza las solicitudes hacia los modelos generativos de Google, gestionando claves, peticiones y respuestas de forma unificada mediante endpoints REST.

Ideal como **puerta de enlace IA local o en red**, integrable con aplicaciones, microservicios o sistemas existentes.


---

## Descripción técnica

IASanic actúa como un **API Gateway** entre tus aplicaciones y la API de **Google Generative AI (Gemini)**.  
Centraliza y gestiona las solicitudes a los modelos de Gemini mediante endpoints REST, facilitando la integración y el control de acceso.

Proporciona endpoints para:
- **Generar texto** directamente desde Gemini.  
- **Analizar y normalizar** consultas del usuario.  
- **Ejecutar flujos RAG (Retrieval-Augmented Generation)** combinando datos locales y contexto dinámico.

Diseñado para arquitecturas de microservicios, puede desplegarse tanto **localmente** como en **entornos de producción** (Nginx + systemd).




---

##  Estructura del proyecto

```bash
iasanic/
 ├── app/
 │   ├── __init__.py
 │   ├── app.py
 │   ├── config.py
 │   ├── services.py
 │   ├── normalizador_funcion.py
 │   └── google_keys.json
 ├── venv/
 └── requirements.txt
```


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






## Despliegue en Producción

A continuación se muestra un ejemplo básico para desplegar IASanic en un servidor Linux:

### 1. Crear servicio systemd

Archivo: `/etc/systemd/system/iasanic.service`

```ini
[Unit]
Description=IASanic Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/iasanic
Environment="PATH=/opt/iasanic/venv/bin"
ExecStart=/opt/iasanic/venv/bin/sanic app.app:app --workers=2 --host=127.0.0.1 --port=8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable iasanic
sudo systemctl start iasanic
sudo systemctl status iasanic
```

### 2. Configurar Nginx como proxy inverso

Archivo: `/etc/nginx/sites-available/iasanic`

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Activar el sitio y reiniciar Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/iasanic /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. (Opcional) Habilitar HTTPS

Instalar y configurar **Certbot** para certificados SSL:

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

Con esto, IASanic quedará desplegado de forma segura y lista para producción.



##  Licencia

Distribuido bajo licencia **MIT**.  
Libre para usar, modificar y distribuir.
