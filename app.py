import streamlit as st
import nltk

# Descargar los recursos necesarios de NLTK
nltk.download('wordnet')
nltk.download('omw-1.4')

# 👇 Esto debe ir aquí, antes de cualquier otra llamada de Streamlit
st.set_page_config(page_title="VocabMaster", layout="centered")

# Luego importa tus módulos
from views import buscar_palabra, repaso_buscadas, repaso_aprendidas, consolidadas

st.title("📘 MasterLex")

# Menú lateral
opcion = st.sidebar.radio(
    "Selecciona una opción",
    [
        "Buscar palabra",
        "Repasar buscadas",
        "Repasar aprendidas",
        "Ver consolidadas"
    ]
)

# Llamada a cada vista
if opcion == "Buscar palabra":
    buscar_palabra.mostrar()

elif opcion == "Repasar buscadas":
    repaso_buscadas.mostrar()

elif opcion == "Repasar aprendidas":
    repaso_aprendidas.mostrar()

elif opcion == "Ver consolidadas":
    consolidadas.mostrar()
