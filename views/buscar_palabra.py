import streamlit as st
import json
import os

from nltk.corpus import wordnet as wn
from utils.api_diccionario import obtener_definicion_en
from utils.api_traduccion import traducir
from utils.api_sinonimos import obtener_sinonimos_en
from utils.nivel_palabra import obtener_nivel_cefr


DATA_PATH = "data/palabras.json"

def cargar_base():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {}

def guardar_base(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


# 🔍 NUEVA función para obtener significados reales de WordNet
def obtener_significados_con_sinonimos(palabra, tipo_pos):
    resultados = []

    for synset in wn.synsets(palabra, pos=tipo_pos):
        definicion = synset.definition()
        sinonimos = list(set([l.name().replace('_', ' ') for l in synset.lemmas()]))
        ejemplos = synset.examples()

        resultados.append({
            "definicion": definicion,
            "sinonimos": sinonimos,
            "ejemplos": ejemplos
        })

    return resultados


def mostrar():
    st.subheader("🔍 Buscar palabra")

    palabra_usuario = st.text_input("Escribe una palabra en inglés o español:")

    if palabra_usuario:
        palabra_en = palabra_usuario.strip()
        palabra_traducida = traducir(palabra_en, target="es")  # DeepL detecta idioma


        if " " not in palabra_en.strip():
            pos, nivel = obtener_nivel_cefr(palabra_en)
            definicion_en = obtener_definicion_en(palabra_en, pos)
            sinonimos_en = obtener_sinonimos_en(palabra_en)

            if not definicion_en:
                st.warning("❌ No se encontró definición.")
                return
        else:
            pos = nivel = "—"
            definicion_en = "❌ No disponible para expresiones."
            sinonimos_en = []

        if sinonimos_en:
            texto_sinonimos = ", ".join(sinonimos_en)
            traduccion_sinonimos = traducir(texto_sinonimos, target="es")
        else:
            traduccion_sinonimos = "—"

        # 🟩 Mostrar encabezado con la palabra
        st.markdown(f"### {palabra_en} ({pos}, {nivel})")

        # 1. Definición
        st.markdown('<span style="color:#4DA6FF; font-size:20px; font-weight:bold;">Definition</span>', unsafe_allow_html=True)
        st.write(definicion_en)

        # 2. Sinónimos en inglés
        st.markdown('<span style="color:#6FCF97; font-size:20px; font-weight:bold;">Synonyms</span>', unsafe_allow_html=True)
        if sinonimos_en:
            st.write(", ".join(sinonimos_en))
        else:
            st.write("No se encontraron sinónimos.")

        # 3. Traducción de la palabra y sinónimos
        with st.expander("Traducción"):
            st.markdown(
                f'<span style="font-weight:bold; font-size:18px">{palabra_traducida}</span>, {traduccion_sinonimos}',
                unsafe_allow_html=True
            )

        # 4. Significados reales con WordNet
        st.markdown('<span style="color:#BB6BD9; font-size:18px; font-weight:bold;">Meanings and synonyms</span>', unsafe_allow_html=True)

        if pos == "noun":
            pos_wordnet = wn.NOUN
        elif pos == "verb":
            pos_wordnet = wn.VERB
        elif pos == "adj":
            pos_wordnet = wn.ADJ
        else:
            pos_wordnet = wn.NOUN  # por defecto

        significados = obtener_significados_con_sinonimos(palabra_en, pos_wordnet)

        if significados:
            for i, item in enumerate(significados[:5], 1):  # muestra los 5 primeros
                st.markdown(f"**{i}. {item['definicion']}**")
                if item["sinonimos"]:
                    st.write("🔁", ", ".join(item["sinonimos"]))
                if item["ejemplos"]:
                    st.caption("💬 Ejemplo: " + item["ejemplos"][0])
        else:
            st.write("No se encontraron significados detallados.")

        # 5. Guardar palabra
        base = cargar_base()
        if palabra_en not in base:
            base[palabra_en] = {
                "original": palabra_usuario,
                "nivel": nivel,
                "pos": pos,
                "definicion_en": definicion_en,
                "definicion_es": traducir(definicion_en, target="es"),
                "sinonimos_en": sinonimos_en,   # ← Asegúrate de que esta línea está
                "estado": "buscada",
                "repaso": []
            }
            guardar_base(base)
            st.success("✅ Palabra guardada correctamente.")
        else:
            st.info("ℹ️ La palabra ya estaba registrada.")
