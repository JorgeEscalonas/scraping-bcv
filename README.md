# Banco Central de Venezuela (BCV) Scraper & API

Este repositorio contiene un servicio en Python para extraer en tiempo real las tasas de cambio oficiales del Dólar (USD) y Euro (EUR) publicadas por el Banco Central de Venezuela. El proyecto puede ejecutarse como un script local o desplegarse como una API RESTfulServerless a través de Vercel.

## Funcionalidades Principales

- Obtención del precio oficial mediante web scraping directo a la plataforma del BCV.
- Resolución de problemas asociados a certificados SSL vencidos o inválidos en la fuente original.
- Implementación de User-Agent gestionado para evitar bloqueos por parte del servidor.
- Estructura preparada para despliegue serverless mediante FastAPI y Vercel.

## Requisitos del Sistema

- Python 3.7 o superior
- Conexión estable a Internet
- Dependencias indicadas en el archivo requirements.txt

## Uso y Ejecución Local

Para ejecutar el servicio localmente, siga los siguientes pasos:

1. Clonar el repositorio:

   ```bash
   git clone <LA_URL_DE_SU_REPOSITORIO>
   cd scraping-bcv
   ```

2. Configurar el entorno virtual (Recomendado):

   ```bash
   python -m venv venv
   
   # Activación en Windows:
   .\venv\Scripts\activate
   
   # Activación en macOS/Linux:
   source venv/bin/activate
   ```

3. Instalar las dependencias requeridas:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar el script base:

   ```bash
   python bcv_scraper.py
   ```

## Despliegue como API en Vercel

El proyecto está configurado para operar como una API utilizando FastAPI. Para su publicación en Vercel:

1. Inicie sesión en Vercel y seleccione la opción para añadir un nuevo proyecto desde GitHub.
2. Seleccione este repositorio de la lista.
3. No es necesario modificar ninguna configuración adicional (Build Command o Output Directory). El archivo `vercel.json` y la carpeta `api/` manejarán el enrutamiento.
4. Presione "Deploy".

Una vez desplegada, la API ofrecerá los siguientes puntos de acceso (endpoints):

- Ruta base `GET /`: Retorna información general sobre la API y su estado.
- Datos de divisas `GET /api/rates`: Retorna un objeto JSON con las tasas de cambio actuales de la siguiente forma:

  ```json
  {
    "success": true,
    "rates": {
      "USD": "valor",
      "EUR": "valor"
    }
  }
  ```

## Consideraciones Técnicas

El script desactiva de forma explícita las advertencias de tipo `InsecureRequestWarning` generadas por la librería `urllib3`. Esta medida es necesaria debido a que la infraestructura web oficial del BCV frecuentemente presenta inconsistencias en sus certificados de seguridad, lo que provocaría interrupciones en el flujo de ejecución estándar si no fuera mitigado.
