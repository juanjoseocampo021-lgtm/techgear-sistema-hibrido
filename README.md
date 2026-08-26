# TechGear - Sistema Híbrido de Catálogo y Pedidos

Sistema web híbrido desarrollado con **FastAPI**, **Django** y **MongoDB Atlas** para la gestión de productos, inventario y pedidos de una tienda de hardware y accesorios tecnológicos.

El proyecto implementa una arquitectura híbrida en la que **FastAPI** funciona como microservicio encargado de la lógica principal del negocio y **Django** funciona como portal web cliente utilizando el patrón **MVT (Models, Views, Templates)**.

---

## 1. Contexto del proyecto

**TechGear** es una tienda especializada en hardware y accesorios tecnológicos.

La empresa requiere un sistema escalable en el que:

* El inventario y los pedidos sean gestionados mediante una API.
* La información se almacene en una base de datos NoSQL en la nube.
* Los clientes puedan consultar el catálogo desde una interfaz web.
* Los usuarios puedan realizar pedidos desde el portal web.
* El sistema controle la disponibilidad del inventario.
* La aplicación pueda ejecutarse tanto localmente como en un entorno de producción.

---

## 2. Objetivo general

Desarrollar e integrar una aplicación web híbrida utilizando:

* **FastAPI** para exponer una API RESTful.
* **MongoDB Atlas** como sistema de almacenamiento NoSQL.
* **Pydantic** para la validación de datos.
* **Django** como portal web utilizando el patrón MVT.
* **Requests** para la comunicación HTTP entre Django y FastAPI.
* **Render** para el despliegue de los servicios.

El sistema permite consultar productos, administrar el inventario y registrar pedidos desde el portal web.

---

# 3. Arquitectura del sistema

El proyecto está dividido en dos componentes principales:

### FastAPI

Funciona como el **backend o API Core** del sistema.

Se encarga de:

* Gestionar productos.
* Gestionar pedidos.
* Validar los datos recibidos.
* Consultar y modificar MongoDB Atlas.
* Validar la disponibilidad del inventario.
* Descontar stock al registrar pedidos.
* Exponer los endpoints REST.
* Proporcionar documentación mediante Swagger UI.

### Django

Funciona como el **portal web cliente**.

Se encarga de:

* Mostrar el catálogo.
* Consumir la API de FastAPI mediante `requests`.
* Renderizar las páginas mediante templates.
* Presentar el formulario de checkout.
* Recibir los datos del cliente.
* Enviar los pedidos hacia FastAPI.
* Mostrar mensajes de éxito y error.

### MongoDB Atlas

Funciona como la base de datos NoSQL del proyecto.

FastAPI utiliza MongoDB Atlas para almacenar:

* Productos.
* Pedidos.

---

# 4. Flujo general de la aplicación

El funcionamiento principal del sistema es:

```text
                 ┌─────────────────────┐
                 │      Usuario        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Django        │
                 │    Portal Web       │
                 └──────────┬──────────┘
                            │
                     HTTP / Requests
                            │
                            ▼
                 ┌─────────────────────┐
                 │      FastAPI        │
                 │      REST API       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   MongoDB Atlas     │
                 │ Productos / Pedidos │
                 └─────────────────────┘
```

### Flujo de creación de pedidos

```text
Usuario
   │
   ▼
Catálogo Django
   │
   ▼
Selecciona producto
   │
   ▼
Checkout
   │
   ▼
Formulario del cliente
   │
   ▼
Django envía POST
   │
   ▼
FastAPI
   │
   ├── Valida producto
   ├── Valida stock
   ├── Calcula/recibe total
   ├── Descuenta inventario
   └── Registra pedido
   │
   ▼
MongoDB Atlas
   │
   ▼
Respuesta de FastAPI
   │
   ▼
Django muestra resultado
```

---

# 5. Estructura del proyecto

```text
TechGear/
│
├── techgear_api/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pedido.py
│   │   └── producto.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── pedidos.py
│   │   └── productos.py
│   │
│   ├── __init__.py
│   ├── database.py
│   └── main.py
│
├── techgear_web/
│   ├── catalogo/
│   │   ├── migrations/
│   │   ├── static/
│   │   │   └── catalogo/
│   │   │       └── css/
│   │   │           └── productos.css
│   │   │
│   │   ├── templates/
│   │   │   └── catalogo/
│   │   │       ├── productos.html
│   │   │       └── checkout.html
│   │   │
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 6. Tecnologías utilizadas

* Python
* FastAPI
* Pydantic
* Motor
* PyMongo
* MongoDB Atlas
* Django
* Requests
* WhiteNoise
* Gunicorn
* Uvicorn
* Git
* GitHub
* Render

---

# 7. Requisitos

Para ejecutar el proyecto localmente se requiere:

* Python 3.14 o compatible.
* Git.
* Cuenta de MongoDB Atlas.
* Navegador web.
* Conexión a Internet.

---

# 8. Instalación

## 8.1 Clonar el repositorio

```bash
git clone https://github.com/juanjoseocampo021-lgtm/techgear-sistema-hibrido.git
cd techgear-sistema-hibrido
```

## 8.2 Crear el entorno virtual

### Windows PowerShell

```powershell
python -m venv venv
```

Activar el entorno:

```powershell
.\venv\Scripts\Activate.ps1
```

## 8.3 Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

# 9. Variables de entorno

Las variables sensibles no deben almacenarse directamente en el código fuente.

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo para ejecución local:

```env
MONGO_URL=tu_url_de_mongodb_atlas
MONGO_DB_NAME=techgear

DJANGO_SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

API_URL=http://127.0.0.1:8000
```

Las credenciales reales de MongoDB Atlas **no deben publicarse en GitHub**.

El archivo `.env` se encuentra excluido mediante `.gitignore`.

---

# 10. Ejecución de FastAPI

Desde la raíz del proyecto:

```powershell
uvicorn techgear_api.main:app --reload
```

La API estará disponible localmente en:

```text
http://127.0.0.1:8000/
```

---

# 11. Swagger UI

FastAPI proporciona automáticamente una interfaz de documentación y pruebas.

Localmente:

```text
http://127.0.0.1:8000/docs
```

Desde Swagger se pueden probar los endpoints de productos y pedidos.

---

# 12. Endpoints principales

## Productos

### Obtener todos los productos

```text
GET /productos/
```

### Obtener un producto

```text
GET /productos/{producto_id}
```

### Crear un producto

```text
POST /productos/
```

### Actualizar un producto

```text
PUT /productos/{producto_id}
```

### Eliminar un producto

```text
DELETE /productos/{producto_id}
```

## Pedidos

### Obtener todos los pedidos

```text
GET /pedidos/
```

### Obtener un pedido

```text
GET /pedidos/{pedido_id}
```

### Crear un pedido

```text
POST /pedidos/
```

---

# 13. Modelos y validación

El proyecto utiliza **Pydantic** para definir y validar los datos.

## Producto

El modelo de producto contiene:

* `id`
* `nombre`
* `descripcion`
* `precio`
* `stock`
* `categoria`

Se aplican validaciones para evitar valores incorrectos, por ejemplo:

* Nombre con longitud mínima.
* Precio mayor que cero.
* Stock igual o superior a cero.

## Pedido

El modelo de pedido contiene:

* `id`
* `cliente`
* `productos`
* `total`
* `estado`

Cada producto dentro del pedido contiene:

* `producto_id`
* `cantidad`

La cantidad debe ser mayor que cero.

---

# 14. Gestión del inventario

Al crear un pedido, FastAPI realiza las validaciones necesarias antes de registrarlo.

El sistema:

1. Verifica que el ID del producto sea válido.
2. Verifica que el producto exista.
3. Comprueba que exista stock suficiente.
4. Descuenta la cantidad solicitada del inventario.
5. Registra el pedido.
6. Devuelve la información del pedido creado.

Si la cantidad solicitada supera el stock disponible, el pedido no se registra y se muestra un mensaje indicando:

```text
La cantidad solicitada supera el stock disponible.
```

---

# 15. Ejecución de Django

Desde la carpeta del proyecto Django:

```powershell
cd techgear_web
```

Ejecutar:

```powershell
python manage.py runserver 8001
```

El portal web estará disponible localmente en:

```text
http://127.0.0.1:8001/
```

---

# 16. Patrón MVT

Django utiliza el patrón **MVT (Models, Views, Templates)**.

En este proyecto:

### Views

Las vistas se encargan de:

* Consumir la API FastAPI.
* Obtener los productos.
* Obtener información de un producto.
* Procesar el formulario de checkout.
* Enviar pedidos mediante HTTP.
* Manejar respuestas y errores.

### Templates

Las plantillas se encargan de:

* Mostrar el catálogo.
* Iterar los productos recibidos.
* Mostrar información de cada producto.
* Mostrar el checkout.
* Mostrar mensajes de éxito y error.

### Forms

Django utiliza un formulario para capturar la información necesaria del cliente y la cantidad solicitada.

---

# 17. Catálogo

El catálogo obtiene los productos directamente desde FastAPI.

La información mostrada incluye:

* Categoría.
* Nombre.
* Descripción.
* Precio.
* Stock disponible.
* Estado del inventario.

El catálogo utiliza Template Tags de Django para recorrer dinámicamente los productos obtenidos desde la API.

---

# 18. Checkout y creación de pedidos

El usuario puede seleccionar un producto desde el catálogo y acceder al checkout.

El formulario permite ingresar información del cliente y seleccionar la cantidad solicitada.

Al confirmar el pedido:

```text
Django
   ↓
POST /pedidos/
   ↓
FastAPI
   ↓
Validación
   ↓
Actualización del stock
   ↓
MongoDB Atlas
   ↓
Respuesta
   ↓
Django
```

El sistema muestra un mensaje de confirmación cuando el pedido es registrado correctamente.

---

# 19. Manejo de errores

El proyecto contempla diferentes situaciones de error.

### API no disponible

Django utiliza manejo de excepciones para evitar que una falla de comunicación con FastAPI genere una pantalla de error para el usuario.

Se muestra un mensaje controlado indicando que no fue posible obtener los productos o registrar el pedido.

### Producto inexistente

FastAPI verifica que el producto exista antes de procesar el pedido.

### ID inválido

Los identificadores de MongoDB son validados antes de realizar las consultas.

### Stock insuficiente

El sistema impide registrar pedidos cuya cantidad supere el inventario disponible.

---

# 20. Archivos estáticos

Los archivos CSS se encuentran dentro de:

```text
techgear_web/catalogo/static/catalogo/
```

Para recopilar los archivos estáticos:

```powershell
python manage.py collectstatic --noinput
```

El proyecto utiliza **WhiteNoise** para servir los archivos estáticos en producción.

---

# 21. Despliegue en Render

El proyecto se encuentra desplegado en Render y fue probado tanto localmente como en producción.

## API FastAPI

```text
https://techgear-api-swth.onrender.com
```

## Portal web Django

```text
https://techgear-web-dzdz.onrender.com
```

## Swagger de la API desplegada

```text
https://techgear-api-swth.onrender.com/docs
```

La aplicación Django desplegada consume la API FastAPI desplegada y utiliza MongoDB Atlas como base de datos.

El flujo de catálogo, checkout, creación de pedidos y actualización de stock fue comprobado también en el entorno desplegado.

---

# 22. Desarrollo por clases

## Clase 1 - Entorno, BD y Modelos Backend

Durante la primera clase se realizó:

* Configuración inicial del proyecto.
* Creación del repositorio Git.
* Creación de la estructura de backend y frontend.
* Configuración del entorno virtual.
* Instalación de dependencias.
* Configuración de MongoDB Atlas.
* Conexión de FastAPI con MongoDB Atlas.
* Creación de los modelos Pydantic de `Producto` y `Pedido`.
* Creación del archivo `requirements.txt`.
* Configuración inicial del repositorio en GitHub.

**Resultado:** estructura inicial del sistema y conexión con la base de datos.

---

## Clase 2 - API REST y Swagger UI

Durante la segunda clase se desarrolló el microservicio FastAPI.

Se implementaron:

* Endpoints de productos.
* Consulta de productos.
* Consulta de producto individual.
* Creación de productos.
* Actualización de productos.
* Eliminación de productos.
* Consulta de pedidos.
* Consulta de pedido individual.
* Creación de pedidos.
* Validación mediante Pydantic.
* Validación de identificadores.
* Validación de existencia de productos.
* Pruebas mediante Swagger UI.

**Resultado:** API REST funcional y lista para ser consumida por Django.

---

## Clase 3 - Django: Setup y Consumo de API

Durante la tercera clase se creó el portal web con Django.

Se realizó:

* Inicialización del proyecto Django.
* Creación de la aplicación `catalogo`.
* Configuración del patrón MVT.
* Configuración de variables de entorno.
* Instalación y configuración de `requests`.
* Comunicación HTTP entre Django y FastAPI.
* Creación de la vista principal.
* Consumo del endpoint de productos.

**Resultado:** integración inicial entre el frontend Django y el backend FastAPI.

---

## Clase 4 - Django: Templates y Catálogo

Durante la cuarta clase se construyó la interfaz visual del catálogo.

Se implementó:

* Template principal del catálogo.
* Uso de Template Tags de Django.
* Renderizado dinámico de productos.
* Visualización de precios.
* Visualización del stock.
* Indicadores de productos disponibles y agotados.
* Diseño mediante CSS.
* Archivos estáticos.
* Configuración de WhiteNoise.
* Preparación para producción.
* Despliegue del portal Django en Render.

**Resultado:** catálogo web funcional, estilizado y desplegado.

---

## Clase 5 - Django: Formularios y Pedidos

Durante la quinta clase se implementó el flujo completo de pedidos.

Se desarrolló:

* Vista de checkout.
* Formulario Django.
* Captura de información del cliente.
* Captura de cantidad.
* Envío de pedidos mediante `POST`.
* Integración con `/pedidos/` de FastAPI.
* Registro de pedidos en MongoDB Atlas.
* Validación del stock.
* Descuento automático del inventario.
* Mensajes de éxito.
* Mensajes de error.
* Pruebas del flujo completo.
* Verificación del funcionamiento local y en Render.

**Resultado:** flujo completo de creación de pedidos integrado entre Django, FastAPI y MongoDB Atlas.

---

## Clase 6 - Refinamiento y Entrega Final

Durante la sexta clase se realizó la revisión final del sistema.

Se verificó:

* Funcionamiento del CRUD de productos.
* Funcionamiento de los pedidos.
* Validación de datos mediante Pydantic.
* Conexión con MongoDB Atlas.
* Validación de stock.
* Descuento de inventario.
* Manejo de productos inexistentes.
* Manejo de identificadores inválidos.
* Manejo de API no disponible.
* Manejo de productos sin stock.
* Flujo completo del checkout.
* Comunicación Django → FastAPI.
* Funcionamiento del catálogo.
* Archivos estáticos y CSS.
* Funcionamiento local.
* Funcionamiento en Render.
* Documentación del proyecto.
* Configuración del repositorio GitHub.

**Resultado:** proyecto final funcional y preparado para entrega.

---

# 23. Pruebas finales realizadas

El sistema fue probado en los siguientes escenarios:

### Catálogo

* Consulta de productos.
* Visualización de información.
* Visualización del stock.
* Visualización de productos agotados.

### Checkout

* Acceso al formulario.
* Validación de campos.
* Selección de cantidad.
* Envío del pedido.

### Pedido exitoso

* Creación del pedido.
* Registro en MongoDB Atlas.
* Consulta mediante `GET /pedidos/`.
* Descuento del stock.

### Stock insuficiente

* Solicitud de una cantidad superior al stock.
* Rechazo del pedido.
* Visualización del mensaje de error.
* No creación del pedido inválido.

### Disponibilidad de la API

* Manejo controlado de errores cuando la API no está disponible.

### Producción

Las pruebas anteriores también fueron realizadas sobre el despliegue en Render.

---

# 24. Control de versiones

El proyecto utiliza **Git y GitHub** como sistema de control de versiones.

Repositorio:

```text
https://github.com/juanjoseocampo021-lgtm/techgear-sistema-hibrido
```

El desarrollo se realizó de manera progresiva utilizando exclusivamente la rama:

```text
main
```

Los cambios se organizaron de acuerdo con las diferentes clases del proyecto.

---

# 25. Criterios de aceptación

El proyecto cumple con los principales criterios establecidos:

* [x] Arquitectura separada entre `techgear_api` y `techgear_web`.
* [x] FastAPI como backend.
* [x] Django como portal web.
* [x] MongoDB Atlas como base de datos.
* [x] Pydantic para validación.
* [x] Swagger UI.
* [x] CRUD de productos.
* [x] Gestión de pedidos.
* [x] Consumo HTTP mediante `requests`.
* [x] Patrón MVT.
* [x] Catálogo dinámico.
* [x] Checkout.
* [x] Validación de stock.
* [x] Actualización del inventario.
* [x] Manejo de excepciones.
* [x] Archivos estáticos.
* [x] WhiteNoise.
* [x] Despliegue en Render.
* [x] Variables sensibles fuera del repositorio.
* [x] README documentado.
* [x] Control de versiones mediante GitHub.
* [x] Trabajo sobre la rama `main`.

---

# 26. Estado final

**TechGear - Sistema Híbrido de Catálogo y Pedidos**

Estado:

**Proyecto final funcional y preparado para entrega.**

El sistema funciona tanto en entorno local como en producción mediante Render, utilizando FastAPI, Django y MongoDB Atlas.

---

## Autores

Proyecto académico desarrollado como parte del **Taller 2 - Sistema Híbrido de Catálogo y Pedidos**.
