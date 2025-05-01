import json
import os

RUTA_NIVELES = os.path.join("data", "niveles_cefr_con_pos.json")

with open(RUTA_NIVELES, "r") as f:
    NIVELES = json.load(f)

def obtener_nivel_cefr(palabra):
    palabra = palabra.lower()
    if palabra in NIVELES:
        info = NIVELES[palabra]
        return info["pos"], info["nivel"]
    else:
        return "—", "—"
