# TechGear - Sistema Híbrido de Catálogo y Pedidos

Sistema web híbrido desarrollado con **FastAPI**, **Django** y **MongoDB Atlas** para la gestión de productos y pedidos de una tienda de hardware y accesorios tecnológicos.

## Arquitectura

El proyecto está dividido en dos componentes principales:

* **FastAPI:** microservicio encargado de la lógica principal del negocio, productos y pedidos.
* **Django:** portal web que consume la API mediante peticiones HTTP y presenta el catálogo mediante el patrón MVT.
* **MongoDB Atlas:** base de datos NoSQL utilizada por FastAPI.

```text
TechGear
│
├── techgear_api/
│   ├── models/
│   ├── routes/
│   ├── database.py
│   └── main.py
│
├── techgear_web/
│   ├── catalogo/
│   │   ├── static/
│   │   ├── templates/
│   │   └── views.py
│   │
│   ├── config/
│   └── manage.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Tecnologías utilizadas

* Python
* FastAPI
* Pydantic
* Motor
* MongoDB Atlas
* Django
* Requests
* WhiteNoise
* Gunicorn
* Uvicorn
* Git y GitHub

## Requisitos

* Python 3.14 o compatible
* Git
* Cuenta de MongoDB Atlas
* Navegador web

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/juanjoseocampo021-lgtm/techgear-sistema-hibrido.git
cd techgear-sistema-hibrido
```

Crear y activar el entorno virtual:

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
MONGO_URL=tu_url_de_mongodb_atlas
MONGO_DB_NAME=techgear
DJANGO_SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
API_URL=http://127.0.0.1:8000
```

Las credenciales reales y contraseñas de MongoDB Atlas **no deben publicarse en GitHub**.

## Ejecutar FastAPI

Desde la raíz del proyecto:

```powershell
uvicorn techgear_api.main:app --reload
```

La API estará disponible localmente en:

```text
http://127.0.0.1:8000/
```

### Swagger UI

La documentación interactiva de FastAPI está disponible en:

```text
http://127.0.0.1:8000/docs
```

## Ejecutar Django

Desde la carpeta `techgear_web`:

```powershell
cd techgear_web
python manage.py runserver 8001
```

El portal web estará disponible en:

```text
http://127.0.0.1:8001/
```

## Archivos estáticos

Los archivos CSS del catálogo se encuentran dentro de:

```text
techgear_web/catalogo/static/catalogo/
```

Para recopilar los archivos estáticos:

```powershell
python manage.py collectstatic --noinput
```

En producción se utiliza **WhiteNoise** para servir los archivos estáticos.

## Despliegue

El proyecto se encuentra desplegado en Render.

### API FastAPI

```text
https://techgear-api-swth.onrender.com
```

### Portal web Django

```text
https://techgear-web-dzdz.onrender.com
```

La API desplegada puede utilizarse para consultar los endpoints disponibles y la aplicación Django consume la API para mostrar el catálogo.

## Control de versiones

El proyecto utiliza GitHub como sistema de control de versiones y trabaja de forma secuencial sobre la rama `main`.

Repositorio:

```text
https://github.com/juanjoseocampo021-lgtm/techgear-sistema-hibrido
```

Los cambios se organizan progresivamente de acuerdo con las clases del proyecto.

## Estado del proyecto

### Clase 1 - Entorno, BD y Modelos Backend

* Estructura inicial del proyecto.
* Configuración de FastAPI.
* Conexión con MongoDB Atlas.
* Modelos Pydantic para productos y pedidos.

### Clase 2 - API REST y Swagger UI

* Endpoints de productos.
* Registro y gestión de pedidos.
* Validación mediante Pydantic.
* Pruebas mediante Swagger UI.

### Clase 3 - Django: Setup y Consumo de API

* Inicialización del proyecto Django.
* Configuración del patrón MVT.
* Consumo de la API FastAPI mediante `requests`.
* Integración entre backend y frontend.

### Clase 4 - Django: Templates y Catálogo

* Construcción y mejora de las plantillas HTML.
* Uso de Template Tags de Django.
* Renderizado del catálogo de productos.
* Implementación de estilos CSS.
* Configuración de archivos estáticos.
* Integración de WhiteNoise para producción.
* Preparación de archivos estáticos mediante `collectstatic`.
* Despliegue funcional del catálogo Django en Render.
