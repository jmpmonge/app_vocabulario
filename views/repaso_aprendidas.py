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

def contar_consolidaciones(lista):
    return sum(1 for item in lista if item == "✓")

def mostrar():
    st.subheader("📗 Repasar palabras aprendidas")

    base = cargar_base()
    aprendidas = {k: v for k, v in base.items() if v["estado"] == "aprendida"}

    if not aprendidas:
        st.info("No hay palabras en estado 'aprendida'.")
        return

    for palabra, datos in aprendidas.items():
        st.markdown(f"### {palabra} ({datos.get('nivel', '—')})")

        with st.expander("Synonym"):
            st.write(", ".join(datos.get("sinonimos_en", [])))

        with st.expander("Definition"):
            st.write(datos.get("definicion_en", ""))

        with st.expander("Traducción"):
            st.write(datos.get("definicion_es", ""))

        st.write("#### Repaso (consolidación):")
        if "repaso" not in datos:
            datos["repaso"] = []

        cols = st.columns(len(datos["repaso"]) + 1 + 1)

        for i, col in enumerate(cols[:-1]):
            with col:
                if i < len(datos["repaso"]):
                    st.markdown(datos["repaso"][i])
                else:
                    if st.button("✓", key=f"{palabra}_ok_apr_{i}"):
                        datos["repaso"].append("✓")
                        if contar_consolidaciones(datos["repaso"]) >= 5:  # 3 previos + 2 nuevos
                            datos["estado"] = "consolidada"
                            st.success(f"{palabra} ha pasado a estado 'consolidada'.")
                        guardar_base(base)
                        st.rerun()

                    if st.button("✗", key=f"{palabra}_fail_apr_{i}"):
                        datos["repaso"].append("✗")
                        guardar_base(base)
                        st.rerun()


        """with cols[-1]:
            if st.button("[+]", key=f"{palabra}_add_apr"):
                datos["repaso"].append("")
                guardar_base(base)
                st.rerun()
        """
