# Banco Central de Venezuela (BCV) API

Una API de alto rendimiento, orientada a arquitecturas Serverless y de código abierto, diseñada para obtener las tasas de cambio oficiales del Banco Central de Venezuela (BCV). Esta implementación provee datos en tiempo real para el Dólar Estadounidense (USD) y el Euro (EUR) a través de un motor automatizado de web scraping, complementado por un panel de control (dashboard) web dedicado.

---

## Tabla de Contenidos

- [Arquitectura y Stack Tecnológico](#arquitectura-y-stack-tecnologico)
- [Características](#caracteristicas)
- [Referencia de Endpoints de la API](#referencia-de-endpoints-de-la-api)
- [Modelos de Datos de Respuesta](#modelos-de-datos-de-respuesta)
- [Desarrollo Local y Configuración](#desarrollo-local-y-configuracion)
- [Despliegue Serverless (Vercel)](#despliegue-serverless-vercel)
- [Consideraciones Técnicas](#consideraciones-tecnicas)

---

## Arquitectura y Stack Tecnológico

El proyecto está estructurado en dos capas principales:

1.  **Backend (Enrutamiento y Procesamiento):** Impulsado por **FastAPI**, un framework web asíncrono construido basado en el tipado estándar de Python. La extracción de datos opera mediante solicitudes HTTP síncronas usando la librería `requests`, y el análisis del DOM mediante `BeautifulSoup4`. Para garantizar un alto rendimiento en instancias Serverless, el motor intenta utilizar el analizador sintáctico `lxml` (escrito en C), degradándose de forma segura y transparente al analizador estándar de Python `html.parser` en caso de que `lxml` no se encuentre disponible.
2.  **Frontend (Dashboard):** Una implementación pura en Vanilla JavaScript, HTML5 y CSS3, servida estáticamente de forma directa a través de la integración nativa de FastAPI (`StaticFiles`). Este panel consume los endpoints internos para presentar un monitor en tiempo real.

---

## Características

-   **Web Scraping en Tiempo Real:** Recupera y analiza la jerarquía precisa del DOM directamente desde la fuente oficial (`www.bcv.org.ve`).
-   **Caché en Memoria (In-Memory Cache):** Implementa un esquema de caché global con un TTL (Time To Live) predefinido de 3600 segundos para mitigar peticiones salientes reiterativas hacia los servidores del BCV, reduciendo drásticamente la latencia en entornos Serverless precalentados (warm starts).
-   **Dashboard Integrado:** Aplicación web dedicada y de diseño responsivo orientada a visualización rápida, generación de recortes de código (snippets) y pruebas del API en vivo.
-   **Endpoints Modulares:** Rutas segmentadas que permiten extraer datos específicos (por ejemplo, obtener exclusivamente la tasa USD), minimizando el peso del payload en la red.
-   **Documentación OpenAPI Automatizada:** Integraciones preconfiguradas con Swagger UI (`/docs`) y ReDoc (`/redoc`), inherentes a la arquitectura de FastAPI.
-   **Evasión Anti-Scraping:** Emulación de cabeceras HTTP (User-Agent) paramétricas y algoritmos de evasión de certificados TLS/SSL para superar bloqueos institucionales de red.

---

## Referencia de Endpoints de la API

Ruta Base: `<HOST_URL>`

### 1. Interfaz Web
-   **`GET /`**
-   **Descripción:** Sirve estáticamente la interfaz de usuario en formato HTML (`api/static/index.html`).

### 2. Payload Completo de Tasas
-   **`GET /api/rates`**
-   **Descripción:** Extrae y devuelve la tasa oficial actual de todas las divisas configuradas (USD y EUR).
-   **Códigos de Estado:**
    -   `200 OK`: Extracción exitosa. Retorna el identificador `success: true` en conjunto con el arreglo serializado de las divisas.
    -   `500 Internal Server Error`: Se detona cuando el servidor alojado por el BCV se encuentra inaccesible, o si las mutaciones en la estructura del DOM rompen las abstracciones del scraper.

### 3. Endpoints de Divisas Aisladas
-   **`GET /api/rates/dolar`**
-   **Descripción:** Filtra el volcado general en memoria para devolver únicamente el payload del Dólar Estadounidense.
-   **Códigos de Estado:** `200 OK`, `404 Not Found`, `500 Internal Server Error`.

-   **`GET /api/rates/euro`**
-   **Descripción:** Filtra el volcado general para devolver únicamente el payload del Euro.
-   **Códigos de Estado:** `200 OK`, `404 Not Found`, `500 Internal Server Error`.

---

## Modelos de Datos de Respuesta

La API retorna información estructurada con estricto apego al siguiente esquema JSON (arreglo de objetos). Dicha estructura replica el "Precio Oficial de las Mesas de Cambio" necesario para flujos de trabajo en software financiero o de comercio electrónico en Venezuela.

### Esquema de Payload (`GET /api/rates`)

```json
{
  "success": true,
  "rates": [
    {
      "fuente": "BCV",
      "nombre": "Dólar",
      "compra": 102.30,
      "venta": 102.30,
      "promedio": 102.30,
      "fechaActualizacion": "2026-03-20T00:00:00-04:00"
    },
    {
      "fuente": "BCV",
      "nombre": "Euro",
      "compra": 110.45,
      "venta": 110.45,
      "promedio": 110.45,
      "fechaActualizacion": "2026-03-20T00:00:00-04:00"
    }
  ]
}
```

*Nota: Para puntos de montaje directos como `/api/rates/dolar`, la constante `rates` empaquetará únicamente un solo objeto dentro del arreglo.*

---

## Desarrollo Local y Configuración

Procedimiento técnico para clonar, depurar (debug) o modificar las capacidades del API en entornos locales:

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/JorgeEscalonas/scraping-bcv.git
    cd scraping-bcv
    ```

2.  **Inicializar el Entorno Virtual:**
    ```bash
    python -m venv venv
    
    # Windows
    .\venv\Scripts\activate
    
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar las Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el Servidor de Desarrollo Local:**
    Levanta la aplicación utilizando Uvicorn como servidor ASGI.
    ```bash
    uvicorn api.index:app --reload
    ```
    El daemon ASGI enlazará por defecto hacia `http://127.0.0.1:8000`. La capa de Frontend se resolverá instantáneamente sobre la ruta raíz, y la especificación OpenAPI de Swagger sobre `/docs`.

---

## Despliegue Serverless (Vercel)

El repositorio incorpora compatibilidad binaria e indexación para ser soportado por las maquinarias *Serverless Runtimes* de Vercel preconfiguradas en Python.

1.  Enlace su cuenta de GitHub en la plataforma automatizada de [Vercel](https://vercel.com).
2.  Haga una importación nativa sin aplicar plantillas externas.
3.  El archivo base de configuración (`vercel.json`) proporcionará las directivas de compilación y compilado. Específicamente, ancla `api/index.py` como el punto de entrada de arranque interno y emite un mandato explícito a los compiladores para incluir y persistir el contenido estático localizado en `api/static/**`.
4.  No se requiere mutar variables de entorno (Environment Variables) ni directivas adicionales de compilación.
5.  Desplegar (Deploy).

---

## Consideraciones Técnicas

### 1. Evasión de Conexiones Seguras TLS (SSL/TLS Handshake Bypass)
El núcleo de raspado (`bcv_scraper.py`) invoca imperativamente la propiedad `urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)`. Tal inyección forma parte de una necesidad arquitectónica. Frecuentemente, las solicitudes cursadas hacia las pasarelas del BCV se enfrentan a expiraciones de certificados y roturas de cadenas de autenticidad que, bajo diseños conservadores, conducirían inminentemente a un error fatal `SSLError`. El script garantiza conectividad paralela desactivando verificaciones hostiles de SSL.

### 2. Resiliencia en Analizadores (Graceful Degradation)
Durante el ciclo de análisis del scraper, el constructor nativo de `BeautifulSoup` intenta inicializar invocando al intérprete `lxml`. En virtud de que ecosistemas Serverless comúnmente excluyen o deprecian librerías nativas parametrizadas en C, la subrutina invoca de forma transparente un cierre `try/except Exception` obligando un retroceso funcional hacia `html.parser` el cual pre-existe implícitamente en librerías Python regulares. Además, aserciones contra NullPointers han sido añadidas para proteger la sustracción del nodo `<div id="dolar">`.

### 3. Limitaciones de Estados Globales en Serverless
El ecosistema de Caché basado en TTL (`_rates_cache`) funciona recluido al entorno en memoria (RAM) atado al runtime de Python. Al desplegar dentro de AWS Lambda (infraestructura basal empleada por Vercel), la retención del caché dura únicamente de acuerdo a la retención del contenedor que da cobijo a un ciclo particular de ejecución (execution environment). Los encendidos en frío ("Cold starts") y las escalas horizontales eludirán el comportamiento en memoria; un diseño implementado buscando minorar de este modo la introducción tecnológica de bases externas de la talla de clusters con Redis In-Memory..
