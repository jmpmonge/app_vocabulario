import streamlit as st
import json
import os

DATA_PATH = "data/palabras.json"

def cargar_base():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {}

def guardar_base(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def tiene_tres_acs_consecutivos(lista):
    return "✓✓✓" in "".join(lista)

def mostrar():
    
    st.subheader("🧠 Repasar palabras buscadas")

    base = cargar_base()
    buscadas = {k: v for k, v in base.items() if v["estado"] == "buscada"}

    if not buscadas:
        st.info("No hay palabras en estado 'buscada'.")
        return

    for palabra, datos in buscadas.items():
        st.markdown(f"### {palabra} ({datos.get('nivel', '—')})")

        with st.expander("Synonym"):
            st.write(", ".join(datos.get("sinonimos_en", [])))

        with st.expander("Definition"):
            st.write(datos.get("definicion_en", ""))

        with st.expander("Sinónimo"):
            st.write(datos.get("definicion_es", ""))

        st.write("#### Repaso:")
        if "repaso" not in datos:
            datos["repaso"] = []

        cols = st.columns(len(datos["repaso"]) + 1 )

        for i, col in enumerate(cols[:-1]):
            with col:
                if i < len(datos["repaso"]):
                    st.markdown(datos["repaso"][i])
                else:
                    if st.button("✓", key=f"{palabra}_ok_{i}"):
                        datos["repaso"].append("✓")
                        if tiene_tres_acs_consecutivos(datos["repaso"]):
                            datos["estado"] = "aprendida"
                            st.success(f"{palabra} ha pasado a estado 'aprendida'.")
                        guardar_base(base)
                        st.rerun()

                    if st.button("✗", key=f"{palabra}_fail_{i}"):
                        datos["repaso"].append("✗")
                        guardar_base(base)
                        st.rerun()

"""
        with cols[-1]:
            if st.button("[+]", key=f"{palabra}_add"):
                datos["repaso"].append("")
                guardar_base(base)
                st.rerun()
"""
