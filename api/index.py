import os
import sys

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Allow importing bcv_scraper from the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bcv_scraper import get_bcv_rates

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="BCV Tipo de Cambio API",
    description="API para obtener los precios del Dólar y Euro desde el Banco Central de Venezuela.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ── Helpers ───────────────────────────────────────────────────────────────────

def _find_rate(nombre: str) -> JSONResponse:
    """Devuelve la tasa de la moneda indicada, o un error 500 si no se pudo obtener."""
    rates = get_bcv_rates()
    if not rates:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "No se pudieron obtener los datos del Banco Central de Venezuela.",
            },
        )

    match = next((r for r in rates if r["nombre"] == nombre), None)
    if not match:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": f"Moneda '{nombre}' no encontrada."},
        )

    return JSONResponse(content={"success": True, "rates": [match]})


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
def index():
    """Serve the web dashboard."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get(
    "/api/rates",
    summary="Todas las tasas",
    description="Devuelve las tasas de cambio del **Dólar** y el **Euro** publicadas por el BCV.",
    tags=["Tasas"],
)
def get_rates():
    """Retorna todas las monedas disponibles."""
    rates = get_bcv_rates()

    if rates:
        return JSONResponse(content={"success": True, "rates": rates})

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "No se pudieron obtener los datos del Banco Central de Venezuela.",
        },
    )


@app.get(
    "/api/rates/dolar",
    summary="Tasa del Dólar",
    description="Devuelve únicamente la tasa oficial del **Dólar Americano (USD)** publicada por el BCV.",
    tags=["Tasas"],
)
def get_dolar():
    """Retorna solo la tasa del Dólar Americano."""
    return _find_rate("Dólar")


@app.get(
    "/api/rates/euro",
    summary="Tasa del Euro",
    description="Devuelve únicamente la tasa oficial del **Euro (EUR)** publicada por el BCV.",
    tags=["Tasas"],
)
def get_euro():
    """Retorna solo la tasa del Euro."""
    return _find_rate("Euro")
