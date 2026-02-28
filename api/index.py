from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys
import os

# Agregamos la ruta principal para poder importar bcv_scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bcv_scraper import get_bcv_rates

# La instancia de FastAPI que Vercel ejecutará
app = FastAPI(
    title="BCV Tipo de Cambio API",
    description="API para obtener los precios del Dólar y Euro desde el Banco Central de Venezuela",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API del BCV",
        "endpoints": {
            "rates": "/api/rates"
        },
        "repository": "https://github.com/JorgeEscalonas/scraping-bcv"
    }

@app.get("/api/rates")
def get_rates():
    """
    Realiza scraping en tiempo real a la página del BCV y devuelve las tasas actuálizadas.
    """
    rates = get_bcv_rates()
    
    if rates:
        return JSONResponse(content={
            "success": True,
            "rates": rates
        })
    else:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Error al extraer los datos del Banco Central de Venezuela."
            }
        )
