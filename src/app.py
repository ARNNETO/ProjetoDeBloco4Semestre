# Importa bibliotecas
import streamlit as st
from pathlib import Path
from data import df_country, df_state, df_temp
from datetime import date
import pandas as pd

# Configura o layout do streamlit
st.set_page_config(layout= 'wide')

#=============================== FUNÇÕES
# Filtra ano do dataframe
def filtra_dataframe(
    dataframe_filtro: pd.DataFrame,
    ano: str,
    filtro_ano
) -> pd.DataFrame:
    df_filtro = dataframe_filtro[
        dataframe_filtro[ano].isin(filtro_ano)
    ]
    return df_filtro
# ------------------------------------------------
# Cria lista de anos
def lista_ano(dataframe_ano):
    return sorted(dataframe_ano["dt"].apply(lambda data: data.year).unique().tolist())
# ------------------------------------------------
# Adiciona coluna ano
def col_ano(
    dataframe_ano: pd.DataFrame,
    coluna_ano: str
) -> pd.DataFrame:
    new_dataframe = dataframe_ano.copy()
    new_dataframe["ano"] = new_dataframe[coluna_ano].apply(
        lambda data: data.year
    )
    return new_dataframe

#=============================== SESSION STATE
# Inicia as preferências antes de criar o session state
if 'cor_fundo' not in st.session_state:
    st.session_state.cor_fundo = '#FFFFFF'
# ------------------------------------------------
if 'cor_fonte' not in st.session_state:
    st.session_state.cor_fonte = '#000000'
# ------------------------------------------------
if 'filtra_ano_country' not in st.session_state:
    st.session_state.filtra_ano_country = False
# ------------------------------------------------
if 'filtra_ano_state' not in st.session_state:
    st.session_state.filtra_ano_state = None
# ------------------------------------------------
if 'filtra_ano_global' not in st.session_state:
    st.session_state.filtra_ano_global = None

#=============================== CARGA DE IMAGEM
# Diretório da imagem
root_dir = Path(__file__).parent.parent
st.title('Monitoramento da Temperatura Global :fire_extinguisher: :fire:',text_alignment="center")
coltext1, coltext2, coltext3, coltext4 = st.columns((6,1,1,1))
with coltext1:
    st.image(root_dir/'util/images/aquecimento-global.jpg',caption='"Quanto mais demorarmos para reduzir as emissões, mais caro vai custar para mantermos o aumento da temperatura em 2ºC". - Rajendra Pachauri, presidente IPCC',width=300)

# =============================== CONFIGURAÇÃO DA PÁGINA
with coltext3:
    st.color_picker("Escolha a cor de fundo:", key="cor_fundo")
with coltext4:
    st.color_picker("Escolha a cor da fonte:", key="cor_fonte")

# Aplica cores de fundo e fonte
st.markdown(
    f"""
    <style>
        /* Cor de fundo da aplicação */
        .stApp {{
            background-color: {st.session_state.cor_fundo};
            color: {st.session_state.cor_fonte};
        }}

        /* Cor dos textos */
        .stApp p,
        .stApp span,
        .stApp label,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {{
            color: {st.session_state.cor_fonte};
        }}
    </style>
    """,
    unsafe_allow_html=True
)
#=============================== VISUALIZAÇÕES
# Exibe amostra dos dataframes
st.subheader('Este painel tem como objetivo monitar o aquecimento global, ajudando na tomada de desição de forma rápida e segura.')
st.markdown('Você pode conferir a fonte dos dados [aqui.](https://www.kaggle.com/datasets/sachinsarkar/climate-change-global-temperature-data)')
st.markdown('Você também pode se aprofundar nos "Objetivos de Desenvolvimento Sustentavel" acessando o [link.](https://conectabrasil.org/home)')
st.write('Amostra do dataset GlobalLandTemperaturesByCountry')
st.dataframe(df_country.head(10))
st.write('Amostra do dataset GlobalLandTemperaturesByState')
st.dataframe(df_state.head(10))
st.write('Amostra do dataset GlobalLandTemperatures')
st.dataframe(df_temp.head(10))

#=============================== SIDEBAR


df_country_ano = col_ano(df_country, "dt")
lista_ano_df_country = lista_ano(df_country_ano)
todos_anos = [" "] + lista_ano_df_country

st.sidebar.header("Filtro")
with st.sidebar:
    seleciona_ano_df_country = st.selectbox('Filtro de Ano do dataset GlobalLandTemperaturesByCountry',options=todos_anos)

if seleciona_ano_df_country == " ":
    df_country_filtrado = df_country_ano
    st.text("Selecionado todos os anos.")
else:
    df_country_filtrado = filtra_dataframe(
        df_country_ano,
        "ano",
        [seleciona_ano_df_country]
    )
    st.text(f"Selecionado o ano {seleciona_ano_df_country}")
st.dataframe(df_country_filtrado)
