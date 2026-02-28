import requests
from bs4 import BeautifulSoup
import urllib3

# Desactivar advertencias de SSL ya que la web del BCV a veces tiene problemas de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bcv_rates():
    url = "https://www.bcv.org.ve/"
    try:
        # Se necesita un User-Agent para que el servidor no rechace la petición (algunos anti-scraping bloquean peticiones sin esto)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # El BCV tiene contenedores específicos para cada moneda
        # Para el dólar:
        dolar_div = soup.find('div', id='dolar')
        dollar_price = "No encontrado"
        if dolar_div:
            dollar_price = dolar_div.find('strong').text.strip()
            
        # Para el euro:
        euro_div = soup.find('div', id='euro')
        euro_price = "No encontrado"
        if euro_div:
            euro_price = euro_div.find('strong').text.strip()
            
        return {'USD': dollar_price, 'EUR': euro_price}
        
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return None

if __name__ == "__main__":
    rates = get_bcv_rates()
    if rates:
        print(f"Dolar (USD): {rates['USD']} Bs.")
        print(f"Euro (EUR): {rates['EUR']} Bs.")
