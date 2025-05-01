import json
from nltk.corpus import wordnet
import nltk

# Solo necesario si aún no lo has hecho:
nltk.download("wordnet")

# Cargar niveles CEFR
with open("data/niveles_cefr.json", "r") as f:
    niveles = json.load(f)

palabras_validas = set(niveles.keys())

def obtener_sinonimos_filtrados(palabra, maximo=5):
    sinonimos = set()
    for syn in wordnet.synsets(palabra):
        for lemma in syn.lemmas():
            nombre = lemma.name().replace("_", " ")
            if nombre.lower() != palabra.lower() and nombre.lower() in palabras_validas:
                sinonimos.add(nombre)
            if len(sinonimos) >= maximo:
                break
        if len(sinonimos) >= maximo:
            break
    return sorted(sinonimos)

resultado = {}
for palabra in sorted(palabras_validas):
    s = obtener_sinonimos_filtrados(palabra)
    if s:
        resultado[palabra] = s

with open("data/sinonimos_educativos_filtrados.json", "w") as f:
    json.dump(resultado, f, indent=2)

print("✅ Archivo 'sinonimos_educativos_filtrados.json' creado correctamente.")
