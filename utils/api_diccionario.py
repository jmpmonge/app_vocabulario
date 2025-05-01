from nltk.corpus import wordnet

# Mapeo para categorías gramaticales
POS_MAP = {
    "noun": wordnet.NOUN,
    "verb": wordnet.VERB,
    "adj": wordnet.ADJ,
    "adjective": wordnet.ADJ,
    "adv": wordnet.ADV,
    "adverb": wordnet.ADV
}

def obtener_definicion_en(palabra, categoria="noun"):
    palabra = palabra.lower()
    pos = POS_MAP.get(categoria.lower(), wordnet.NOUN)

    synsets = wordnet.synsets(palabra, pos=pos)
    if not synsets:
        return None
    return synsets[0].definition()
