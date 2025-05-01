import requests
import streamlit as st

APP_ID = st.secrets["oxford"]["app_id"]
APP_KEY = st.secrets["oxford"]["app_key"]

def buscar_en_oxford(palabra, idioma="en-us"):
    url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/{idioma}/{palabra.lower()}"

    headers = {
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        data = res.json()
        try:
            entrada = data["results"][0]["lexicalEntries"][0]
            nivel = entrada.get("cefrLevel", "—")
            definicion = entrada["entries"][0]["senses"][0]["definitions"][0]

            # Extraer sinónimos si existen
            sinonimos = []
            senses = entrada["entries"][0]["senses"]
            for sense in senses:
                if "synonyms" in sense:
                    sinonimos.extend([s["text"] for s in sense["synonyms"]])
                if len(sinonimos) >= 5:
                    break

            return {
                "nivel": nivel,
                "definicion": definicion,
                "sinonimos_en": sinonimos[:5]
            }
        except Exception as e:
            return {"error": f"No se pudo extraer datos: {e}"}
    else:
        return {"error": f"Oxford API error: {res.status_code}"}
