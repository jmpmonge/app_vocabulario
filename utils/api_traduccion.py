import streamlit as st
import requests

API_KEY = st.secrets["api"]["deepl_key"]

def traducir(texto, target="es"):
    # st.write("🟡 Paso 1: Texto recibido para traducir:", texto)

    url = "https://api-free.deepl.com/v2/translate"
    texto_limpio = texto.strip()

    # st.write("🟡 Paso 2: Texto limpio (sin espacios extremos):", texto_limpio)

    if not texto_limpio:
        # st.warning("⚠️ No has introducido ningún texto para traducir.")
        return "[VACÍO]"

    data = {
        "auth_key": API_KEY,
        "text": texto_limpio,
        "target_lang": target.upper()
    }

    # st.write("🟡 Paso 3: Datos que se enviarán a DeepL:", data)

    try:
        res = requests.post(url, data=data, timeout=5)
        # st.write("🟢 Paso 4: Respuesta de DeepL recibida. Código:", res.status_code)
        res.raise_for_status()

        resultado = res.json()
        # st.write("🟢 Paso 5: JSON recibido de DeepL:", resultado)

        traduccion = resultado["translations"][0]["text"]
        # idioma_detectado = resultado["translations"][0]["detected_source_language"]

        # st.success(f"🌍 Idioma detectado por DeepL: {idioma_detectado}")
        # st.success(f"✅ Traducción final: {traduccion}")

        return traduccion

    except Exception as e:
        # st.error(f"🔴 Error al traducir: {e}")
        return "[ERROR]"
