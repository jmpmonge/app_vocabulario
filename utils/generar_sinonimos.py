import json
from nltk.corpus import wordnet

# (solo necesario la primera vez)
import nltk
nltk.download('wordnet')

# Cargar niveles
with open("data/niveles_cefr.json", "r") as f:
    niveles = json.load(f)

def obtener_sinonimos(palabra, maximo=3):
    sinonimos = set()
    for syn in wordnet.synsets(palabra):
        for lemma in syn.lemmas():
            s = lemma.name().replace('_', ' ')
            if s.lower() != palabra.lower():
                sinonimos.add(s)
            if len(sinonimos) >= maximo:
                break
        if len(sinonimos) >= maximo:
            break
    return sorted(sinonimos)

# Generar diccionario
sinonimos = {}
for palabra in sorted(niveles.keys()):
    s = obtener_sinonimos(palabra)
    if s:
        sinonimos[palabra] = s

# Guardar
with open("data/sinonimos_educativos.json", "w") as f:
    json.dump(sinonimos, f, indent=2)

print("✅ Archivo 'sinonimos_educativos.json' generado correctamente.")
