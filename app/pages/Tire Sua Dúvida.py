import os

import pandas as pd
import requests
import streamlit as st

from data.processed import carregar_temperaturas_pais, coletar_texto, garantir_csvs

API = os.getenv("CLIMATE_API_URL", "http://127.0.0.1:8000").rstrip("/")


def consultar_api(rota, entrada, campo_resposta):
    try:
        with st.spinner("Consultando o modelo local..."):
            resposta = requests.post(f"{API}/{rota}", json=entrada, timeout=(3, 100))
    except requests.Timeout:
        st.error("A API demorou para responder. Tente uma entrada menor.")
        return None
    except requests.RequestException:
        st.error("Não foi possível conectar ao FastAPI.")
        return None

    try:
        dados = resposta.json()
    except ValueError:
        dados = {}

    if isinstance(dados, dict):
        if resposta.ok and isinstance(dados.get(campo_resposta), str):
            return dados[campo_resposta]
        if isinstance(dados.get("detail"), str):
            st.error(dados["detail"])
            return None

    st.error("A API retornou uma resposta inesperada.")
    return None


def contexto_temperatura():
    try:
        garantir_csvs("GlobalLandTemperaturesByCountry.csv")
        dados = carregar_temperaturas_pais()
    except (OSError, ValueError, ImportError, RuntimeError, requests.RequestException):
        st.error("Confira os CSVs em app/data/datasets e o acesso ao Kaggle.")
        return ""

    paises = sorted(dados["Country"].dropna().unique())
    if not paises:
        st.warning("O CSV não contém países válidos.")
        return ""

    pais = st.selectbox("País", paises, index=paises.index("Brazil") if "Brazil" in paises else 0)
    recorte = dados.loc[dados["Country"] == pais].copy()
    recorte["ano"] = pd.to_datetime(recorte["dt"]).dt.year
    anos = sorted(recorte["ano"].dropna().unique().tolist())
    escolhidos = st.multiselect("Anos", anos, default=anos[:3], max_selections=8)
    bruto = recorte[recorte["ano"].isin(escolhidos)]
    limpo = (
        bruto.dropna(subset=["AverageTemperature"])
        .drop_duplicates(subset=["dt", "AverageTemperature"])
    )
    # Se houver mais de uma temperatura na mesma data, exclui a data que causa conflito.
    limpo = limpo[~limpo["dt"].duplicated(keep=False)]
    resumo = limpo.groupby("ano").agg(
        media=("AverageTemperature", "mean"),
        meses=("dt", "nunique"),
    ).reindex(sorted(escolhidos))
    resumo["media"] = resumo["media"].round(2)
    resumo["meses"] = resumo["meses"].fillna(0).astype(int)

    st.markdown(
        "Fonte: [Kaggle — Climate Change Global Temperature Data]"
        "(https://www.kaggle.com/datasets/sachinsarkar/climate-change-global-temperature-data)"
    )
    with st.expander("Registros do CSV no recorte"):
        st.dataframe(bruto.drop(columns="ano"))
    with st.expander("Registros usados no cálculo"):
        st.dataframe(limpo)
    st.caption(f"{len(bruto)} registros no recorte e {len(limpo)} após a limpeza.")
    if limpo.empty:
        st.info("Selecione anos com medições válidas para consultar o modelo.")
        return ""

    st.dataframe(resumo.rename(columns={"media": "Média (°C)", "meses": "Meses válidos"}))
    st.bar_chart(resumo[["media"]].rename(columns={"media": "Média (°C)"}), x_label="Ano")
    st.caption("A média usa os meses disponíveis. Compare anos com cobertura semelhante.")
    linhas = [
        f"{ano}: {linha.media:.2f} °C, {int(linha.meses)} meses válidos."
        if linha.meses else f"{ano}: sem medições válidas."
        for ano, linha in resumo.iterrows()
    ]
    return (
        f"Fonte: CSV GlobalLandTemperaturesByCountry.csv (Kaggle). País: {pais}. "
        "Médias simples das temperaturas mensais disponíveis. "
        "Verifique a cobertura de meses antes de comparar anos.\n" + "\n".join(linhas)
    )


st.set_page_config(layout="wide")
st.title("Tire Sua Dúvida")
modo = st.radio("O que você quer fazer?", ["Conversar com os dados", "Resumir um texto"])

if modo == "Resumir um texto":
    with st.form("resumo_local"):
        texto = st.text_area("Texto do boletim ou da reportagem", max_chars=2000)
        enviar = st.form_submit_button("Gerar resumo")
    if enviar:
        st.session_state.pop("resumo_local_resultado", None)
        if texto.strip():
            resumo = consultar_api("processar_texto", {"texto": texto}, "texto_processado")
            if resumo:
                st.session_state.resumo_local_resultado = resumo
        else:
            st.warning("Digite ou cole um texto.")
    if "resumo_local_resultado" in st.session_state:
        st.text(st.session_state.resumo_local_resultado)
    st.stop()

fonte = st.selectbox(
    "Fonte para a conversa", ["Temperatura por país", "Reportagem sobre calor", "Boletim de queimadas"]
)
contexto = ""
if fonte == "Temperatura por país":
    contexto = contexto_temperatura()
elif fonte == "Reportagem sobre calor":
    st.markdown("Fonte: [Blog da Raia](https://www.drogaraia.com.br/blog/saude/longevidade/calor-intenso)")
    try:
        reportagem = coletar_texto()
        if reportagem:
            contexto = "Fonte: Blog da Raia, reportagem Calor Intenso. Trecho inicial:\n" + reportagem[:1700]
        else:
            st.info("A reportagem não contém texto disponível para consulta.")
    except (requests.RequestException, ValueError):
        st.warning("Reportagem indisponível no momento.")
else:
    boletim = st.text_area("Cole um trecho do boletim e inclua a fonte e a data", max_chars=1700)
    if boletim.strip():
        contexto = "Fonte: boletim informado pelo usuário.\n" + boletim.strip()

if not contexto:
    st.stop()

with st.expander("Material enviado ao modelo"):
    st.text(contexto)

if st.session_state.get("contexto_conversa") != contexto:
    st.session_state.contexto_conversa = contexto
    st.session_state.turnos_conversa = []

st.caption("As respostas usam até três turnos recentes. Ao trocar o recorte ou o texto, a conversa é reiniciada.")
if st.button("Limpar conversa"):
    st.session_state.turnos_conversa = []

for turno in st.session_state.turnos_conversa:
    with st.chat_message("user"):
        st.text(turno["pergunta"])
    with st.chat_message("assistant"):
        st.text(turno["resposta"])

pergunta = st.chat_input("Pergunte sobre o recorte selecionado", max_chars=500)
if pergunta and pergunta.strip():
    pergunta = pergunta.strip()
    with st.chat_message("user"):
        st.text(pergunta)
    resposta = consultar_api(
        "conversar",
        {
            "pergunta": pergunta,
            "contexto": contexto,
            "historico": st.session_state.turnos_conversa[-3:],
        },
        "resposta",
    )
    if resposta:
        st.session_state.turnos_conversa.append({"pergunta": pergunta, "resposta": resposta})
        with st.chat_message("assistant"):
            st.text(resposta)
