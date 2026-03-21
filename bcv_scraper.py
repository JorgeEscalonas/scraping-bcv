import time
import urllib3
import requests
from bs4 import BeautifulSoup

# Desactivar advertencias de SSL ya que la web del BCV a veces tiene problemas de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Opciones de caché (1 hora por defecto)
CACHE_TTL = 3600
_rates_cache = None
_cache_timestamp = 0


def _parse_rate(rate_str: str) -> float:
    """Convierte un string de tasa de cambio venezolana a float."""
    try:
        if not rate_str:
            return 0.0
        # El BCV usa comas para los decimales
        return float(rate_str.replace('.', '').replace(',', '.'))
    except ValueError:
        return 0.0


def get_bcv_rates(force_refresh: bool = False):
    """Obtiene las tasas de cambio desde la página oficial del BCV."""
    global _rates_cache, _cache_timestamp
    
    # Validar si el caché aún es válido
    if not force_refresh and _rates_cache and (time.time() - _cache_timestamp < CACHE_TTL):
        return _rates_cache

    url = "https://www.bcv.org.ve/"
    try:
        # User-Agent necesario para que el servidor no rechace la petición (anti-scraping)
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        
        # lxml es más ágil. Si no está instalado, hace fallback a html.parser
        try:
            soup = BeautifulSoup(response.text, 'lxml')
        except Exception:
            # Fallback seguro a html.parser si lxml falla o no se encuentra
            soup = BeautifulSoup(response.text, 'html.parser')

        # Fecha de actualización
        fecha_container = soup.find('div', class_='pull-right dinpro center')
        fecha_actualizacion = "No disponible"
        if fecha_container and fecha_container.find('span'):
            fecha_actualizacion = fecha_container.find('span').get('content', "No disponible")

        # Para el dólar:
        dolar_div = soup.find('div', id='dolar')
        dollar_price = 0.0
        if dolar_div and dolar_div.find('strong'):
            dollar_price = _parse_rate(dolar_div.find('strong').text.strip())
            
        # Para el euro:
        euro_div = soup.find('div', id='euro')
        euro_price = 0.0
        if euro_div and euro_div.find('strong'):
            euro_price = _parse_rate(euro_div.find('strong').text.strip())
            
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
        
    except requests.RequestException as e:
        print(f"Error HTTP al obtener los datos del BCV: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar los datos: {e}")
        return None

if __name__ == "__main__":
    import json
    rates = get_bcv_rates()
    if rates:
        print(json.dumps(rates, indent=2, ensure_ascii=False))
