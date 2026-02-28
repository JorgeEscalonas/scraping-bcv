# Banco Central de Venezuela (BCV) API

Una API Serverless rápida, confiable y de código abierto para obtener el tipo de cambio oficial del Banco Central de Venezuela (BCV), proporcionando las tasas oficiales para el Dólar (USD) y el Euro (EUR).

---

## 📌 Tabla de Contenidos

- [Características](#características)
- [Uso Comercial y Formato de Respuesta](#uso-comercial-y-formato-de-respuesta)
- [Documentación de la API (Endpoints)](#documentación-de-la-api-endpoints)
- [Instalación y Despliegue Local](#instalación-y-despliegue-local)
- [Despliegue en Vercel (Serverless)](#despliegue-en-vercel-serverless)
- [Consideraciones Técnicas](#consideraciones-técnicas)

---

## Características

- Web scraping directo a la fuente oficial (`www.bcv.org.ve`) en tiempo real.
- Bypass estructurado para incidencias de certificados SSL/TLS inherentes a los portales gubernamentales.
- Formato de respuesta JSON optimizado en un esquema Array-Object para facilitar la iteración desde el Frontend.
- Construido con **FastAPI**, listo para despliegues Serverless mediante Vercel (AWS Lambda).

---

## Uso Comercial y Formato de Respuesta

La API retorna un modelo de datos estructurado ideal para integraciones financieras, comercio electrónico y facturación en Venezuela. Se devuelve un arreglo `[]` con objetos por cada divisa, consolidando y replicando el **Precio Oficial de las Mesas de Cambio** para los valores de `compra`, `venta` y `promedio`.

El formato exacto es el siguiente:

```json
[
  {
    "fuente": "BCV",
    "nombre": "Dólar",
    "compra": 419.9873,
    "venta": 419.9873,
    "promedio": 419.9873,
    "fechaActualizacion": "2026-03-02T00:00:00-04:00"
  },
  {
    "fuente": "BCV",
    "nombre": "Euro",
    "compra": 495.60601336,
    "venta": 495.60601336,
    "promedio": 495.60601336,
    "fechaActualizacion": "2026-03-02T00:00:00-04:00"
  }
]
```

---

## Documentación de la API (Endpoints)

Una vez que el proyecto esté en ejecución (ya sea en un entorno local o alojado en Vercel), la API expone los siguientes puntos de acceso:

### `GET /`

- **Descripción**: Endpoint de verificación de salud (healthcheck). Retorna la versión y rutas disponibles.
- **Respuesta Exitosa (200 OK)**:

  ```json
  {
    "message": "Bienvenido a la API del BCV",
    "endpoints": {
      "rates": "/api/rates"
    },
    ...
  }
  ```

### `GET /api/rates`

- **Descripción**: Extrae y retorna el tipo de cambio oficial al momento exacto de la petición.
- **Códigos de estado**:
  - `200 OK`: La extracción fue exitosa. Devuelve un objeto con la llave `success: true` y el arreglo de `rates` descrito en la sección anterior.
  - `500 Internal Server Error`: Ocurrió un fallo en el scraper al intentar leer el portal del BCV (usualmente asociado a la caída general de la página fuente).

---

## Instalación y Despliegue Local

Para modificar o probar la API en un entorno cerrado:

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/JorgeEscalonas/scraping-bcv.git
   cd scraping-bcv
   ```

2. **Entorno Virtual** (Extremadamente recomendado):

   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS / Linux:
   source venv/bin/activate
   ```

3. **Instalación de dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el Scraper de prueba en Terminal**:

   ```bash
   python bcv_scraper.py
   ```

5. **Levantar el Servidor FastAPI Local**:

   ```bash
   uvicorn api.index:app --reload
   ```

   *El servidor estará disponible en `http://127.0.0.1:8000`*

---

## Despliegue en Vercel (Serverless)

Este repositorio está preparado nativamente para su despliegue en Vercel, aprovechando su entorno optimizado de Python Serverless.

1. Registre una cuenta o inicie sesión en [Vercel](https://vercel.com).
2. Agregue un nuevo **Proyecto** e importe este repositorio desde su cuenta de GitHub.
3. El archivo `vercel.json` autoconfigurará las rutas y los build-flags. **No modifique ningún parámetro de Build & Development Settings**.
4. Presione **Deploy**.

En menos de dos minutos, su API estará disponible globalmente en una URL segura HTTPS proporcionada por Vercel.

---

## Consideraciones Técnicas

**Resolución de SSL**: El modelo base (`bcv_scraper.py`) invoca explícitamente `urllib3.disable_warnings`. Esta arquitectura no es un descuido de seguridad, sino una necesidad intrínseca dadas las intermitencias y firmas no verificadas de los hostings gubernamentales del BCV que forzarían la terminación de `requests` con la excepción `SSLError`.
