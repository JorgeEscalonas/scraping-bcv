import requests
from bs4 import BeautifulSoup
import urllib3

# Desactivar advertencias de SSL ya que la web del BCV a veces tiene problemas de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time

# Opciones de caché (1 hora por defecto)
CACHE_TTL = 3600
_rates_cache = None
_cache_timestamp = 0

def get_bcv_rates(force_refresh=False):
    global _rates_cache, _cache_timestamp
    
    # Validar si el caché aún es válido
    if not force_refresh and _rates_cache and (time.time() - _cache_timestamp < CACHE_TTL):
        return _rates_cache

    url = "https://www.bcv.org.ve/"
    try:
        # Se necesita un User-Agent para que el servidor no rechace la petición (algunos anti-scraping bloquean peticiones sin esto)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        
        # lxml es considerablemente más ágil que html.parser si está instalado, útil para Serverless. 
        # Si no, hace fallback elegante a html.parser
        try:
            soup = BeautifulSoup(response.text, 'lxml')
        except:
            soup = BeautifulSoup(response.text, 'html.parser')

        # Fecha de actualizacion
        fecha_container = soup.find('div', class_='pull-right dinpro center')
        fecha_actualizacion = "No disponible"
        if fecha_container and fecha_container.find('span'):
            fecha_actualizacion = fecha_container.find('span')['content'] # Ejemplo: 2026-03-02T00:00:00-04:00
            
        # El BCV tiene contenedores específicos para cada moneda
        # Función auxiliar para formatear la tasa a float
        def parse_rate(rate_str):
            try:
                # El BCV usa comas para los decimales
                return float(rate_str.replace('.', '').replace(',', '.'))
            except:
                return 0.0

        # Para el dólar:
        dolar_div = soup.find('div', id='dolar')
        dollar_price = 0.0
        if dolar_div:
            dollar_price = parse_rate(dolar_div.find('strong').text.strip())
            
        # Para el euro:
        euro_div = soup.find('div', id='euro')
        euro_price = 0.0
        if euro_div:
            euro_price = parse_rate(euro_div.find('strong').text.strip())
            
        # Construir la respuesta con el esquema requerido
        result = [
            {
                "fuente": "BCV",
                "nombre": "Dólar",
                "compra": dollar_price,
                "venta": dollar_price,
                "promedio": dollar_price,
                "fechaActualizacion": fecha_actualizacion
            },
            {
                "fuente": "BCV",
                "nombre": "Euro",
                "compra": euro_price,
                "venta": euro_price,
                "promedio": euro_price,
                "fechaActualizacion": fecha_actualizacion
            }
        ]
        
        # Guardar en caché
        _rates_cache = result
        _cache_timestamp = time.time()
        
        return result
        
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return None

if __name__ == "__main__":
    import json
    rates = get_bcv_rates()
    if rates:
        print(json.dumps(rates, indent=2, ensure_ascii=False))
