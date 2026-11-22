import os

import requests
import streamlit as st

st.title("Tire Sua Dúvida")
st.write("Escreva o que você deseja saber sobre queimadas ou sobre o clima")


with st.form("resposta_local"):
    texto = st.text_area("Texto para gerar resposta", max_chars=300, height=220)
    enviar = st.form_submit_button("Gerar resposta")

if enviar:
    if not texto.strip():
        st.warning("Digite ou cole um texto para gerar resposta.")
        st.stop()

    api = os.getenv("CLIMATE_API_URL", "http://127.0.0.1:8000").rstrip("/")
    try:
        with st.spinner("Gerando resposta..."):
            resposta = requests.post(
                f"{api}/processar_texto", json={"texto": texto}, timeout=(3, 100)
            )
    except requests.Timeout:
        st.error("A API demorou para responder. Tente um trecho menor.")
    except requests.RequestException:
        st.error("Não foi possível conectar à API. Verifique se o FastAPI está em execução.")
    else:
        try:
            dados = resposta.json()
        except requests.exceptions.JSONDecodeError:
            dados = {}

        if resposta.ok and isinstance(dados, dict) and isinstance(dados.get("texto_processado"), str):
            st.subheader("Resposta")
            st.text(dados["texto_processado"])
        else:
            detalhe = dados.get("detail") if isinstance(dados, dict) else None
            st.error(detalhe if isinstance(detalhe, str) else "A API retornou uma resposta inesperada.")
