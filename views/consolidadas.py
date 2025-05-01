import streamlit as st
import json
import os

DATA_PATH = "data/palabras.json"

def cargar_base():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {}

def mostrar():
    st.subheader("🏁 Palabras consolidadas")

    base = cargar_base()
    consolidadas = {k: v for k, v in base.items() if v["estado"] == "consolidada"}

    if not consolidadas:
        st.info("No hay palabras consolidadas aún.")
        return

    for palabra, datos in consolidadas.items():
        st.markdown(f"### {palabra} ({datos.get('nivel', '—')})")

        with st.expander("Synonym"):
            st.write(", ".join(datos.get("sinonimos_en", [])))

        with st.expander("Definition"):
            st.write(datos.get("definicion_en", ""))

        with st.expander("Traducción"):
            st.write(datos.get("definicion_es", ""))

        st.write("#### Historial de repaso:")
        st.markdown(" ".join(datos.get("repaso", [])))
