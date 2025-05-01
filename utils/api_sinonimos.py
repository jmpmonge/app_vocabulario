import json
import os

# Ruta al nuevo archivo filtrado
RUTA_SINONIMOS = os.path.join("data", "sinonimos_educativos_filtrados.json")

# Cargar una vez al inicio
with open(RUTA_SINONIMOS, "r") as f:
    SINONIMOS = json.load(f)

def obtener_sinonimos_en(palabra, maximo=5):
    palabra = palabra.lower()
    return SINONIMOS.get(palabra, [])[:maximo]

