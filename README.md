# Banco Central de Venezuela (BCV) Scraper

Este es un simple y efectivo script en Python para **extraer en tiempo real las tasas de cambio del Dólar (USD) y Euro (EUR)** publicadas por el Banco Central de Venezuela.

## ✨ Funcionalidades
- **Obtención de precio oficial** mediante scraping a la web del BCV (`bcv.org.ve`).
- Solucionado el problema con los certificados SSL vencidos/inválidos comunes en páginas del estado.
- Manejo explícito del `User-Agent` para esquivar bloqueos básicos de protección del servidor.

## 🛠️ Requisitos
- Python 3.7 o superior
- Conexión a Internet
- `requests`
- `beautifulsoup4`

## 🚀 Cómo ejecutarlo
1. Clona o descarga este repositorio:
   ```bash
   git clone <TU_ENLACE_GITHUB>
   ```

2. (Opcional) Crea y activa un entorno virtual (muy recomendado):
   ```bash
   python -m venv venv
   # Activa (En Windows)
   .\venv\Scripts\activate
   # Activa (En Mac / Linux)
   source venv/bin/activate
   ```

3. Instala las dependencias listadas:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el script:
   ```bash
   python bcv_scraper.py
   ```

## ⚠️ Advertencia Técnica

Durante la ejecución, este script desactiva temporalmente las advertencias de "InsecureRequestWarning" (`urllib3.disable_warnings`). Esto fue intencionalmente agregado ya que los certificados de seguridad del BCV a menudo están defectuosos y `requests` devolverá un fallo sin esta corrección visual.
