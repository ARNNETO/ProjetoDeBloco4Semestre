# Importa bibliotecas
import streamlit as st
from pathlib import Path
from data import df_country, df_state, df_temp
from datetime import date
import pandas as pd
from matplotlib.pyplot import plot
import altair as alt

# Configura o layout do streamlit
st.set_page_config(layout= 'wide')

#=============================== FUNÇÕES
# Filtra ano do dataframe
# def filtra_dataframe(
#     dataframe_filtro: pd.DataFrame,
#     ano: str,
#     filtro_ano
# ) -> pd.DataFrame:
#     df_filtro = dataframe_filtro[
#         dataframe_filtro[ano].isin(filtro_ano)
#     ]
#     return df_filtro
# ------------------------------------------------
# Filtra país
def filtra_dataframe_v2(
    dataframe_pais: pd.DataFrame,
    coluna: str,
    dado_filtrado
) -> pd.DataFrame:
    df_filtrado = dataframe_pais[
        dataframe_pais[coluna].isin(dado_filtrado)
    ]
    return df_filtrado
# ------------------------------------------------
# Cria lista de anos
def lista_ano(dataframe_ano):
    return sorted(dataframe_ano["dt"].apply(lambda data: data.year).unique().tolist())
# ------------------------------------------------
# Cria lista
def lista_opcoes(dataframe_lista: pd.DataFrame,
                 coluna: str) -> pd.DataFrame:
    return sorted(dataframe_lista[coluna].unique().tolist())
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
#=============================== AJUSTA DATAFRAMES
# # Cria os dataframes COUNTRY para exibir os dados e gráficos
# df_country_ano = col_ano(df_country, "dt")
# lista_ano_df_country = lista_ano(df_country_ano)
# todos_anos = [" "] + lista_ano_df_country

df_country_graf = df_country[["dt","AverageTemperature", "Country"]]
lista_opcoes_df_country = lista_opcoes(df_country_graf,"Country")
# ------------------------------------------------

#=============================== SIDEBAR
st.sidebar.header("Filtros")
with st.sidebar:
    # seleciona_ano_df_country = st.selectbox('Filtro de Ano do dataset GlobalLandTemperaturesByCountry',options=todos_anos)
    seleciona_pais_df_country = st.multiselect("Por país",options=lista_opcoes_df_country,default=["Brazil"])

#=============================== APLICA OS FILTROS
df_country_filtrado = df_country[df_country["Country"].isin(seleciona_pais_df_country)]
df_country_graf_aplic = df_country_graf[df_country_graf["Country"].isin(seleciona_pais_df_country)] 

#=============================== VISUALIZAÇÕES
# Exibe amostra dos dataframes
st.subheader('Este painel tem como objetivo monitar o aquecimento global a partir do ano 2000, ajudando na tomada de desição de forma rápida e segura.')
st.markdown('Você pode conferir a fonte dos dados [aqui.](https://www.kaggle.com/datasets/sachinsarkar/climate-change-global-temperature-data)')
st.markdown('Você também pode se aprofundar nos "Objetivos de Desenvolvimento Sustentavel" acessando o [link.](https://conectabrasil.org/home)')
st.markdown("---")
# ------------------------------------------------
st.subheader('Aqui podemos observar a temperatura média por país. ')
# st.dataframe(df_country.head(10))
st.text("Temos os dados detalhados:")
st.dataframe(df_country_filtrado)
st.text("Podemos ver a média de temperadora por país selecionado")
line_chart = alt.Chart(df_country_graf_aplic).mark_line(interpolate='basis').encode(
    alt.X("dt", title='Data'),
    alt.Y('AverageTemperature', title='Temperatura'),
    color=alt.Color("Country:N", title="País"),
            tooltip=[
            alt.Tooltip("dt:T", title="Data"),
            alt.Tooltip("AverageTemperature:Q", title="Temperatura"), 
            alt.Tooltip("Country:N", title="País")
        ]
).properties(
        title=alt.TitleParams(
            text="Temperatura Média",
            anchor="middle"
        )
)
st.altair_chart(line_chart) 
st.markdown("---")
# ------------------------------------------------

st.write('Amostra do dataset GlobalLandTemperaturesByState')
st.dataframe(df_state.head(10))
st.write('Amostra do dataset GlobalLandTemperatures')
st.dataframe(df_temp.head(10))

# #=============================== SIDEBAR
# df_country_ano = col_ano(df_country, "dt")
# lista_ano_df_country = lista_ano(df_country_ano)
# todos_anos = [" "] + lista_ano_df_country

# df_country_graf = df_country_ano[["dt","AverageTemperature", "Country"]]
# lista_opcoes_df_country = lista_opcoes(df_country_graf,"Country")

# st.sidebar.header("Filtro")
# with st.sidebar:
#     # seleciona_ano_df_country = st.selectbox('Filtro de Ano do dataset GlobalLandTemperaturesByCountry',options=todos_anos)
#     seleciona_pais_df_country = st.multiselect("Filtro país",options=lista_opcoes_df_country,default=["Brazil"])


#=============================== EXIBE DADOS FILTRADOS
# if seleciona_ano_df_country == " ":
#     df_country_filtrado = df_country_ano
#     st.text("Selecionado todos os anos.")
# else:
#     df_country_filtrado = filtra_dataframe_v2(
#         df_country_ano,
#         "ano",
#         [seleciona_ano_df_country]
#     )
#     st.text(f"Selecionado o ano {seleciona_ano_df_country}")
# st.dataframe(df_country_filtrado)

# df_country_filtrado = df_country[df_country["Country"].isin(seleciona_pais_df_country)]
# st.dataframe(df_country_filtrado)
# # ------------------------------------------------
# df_country_graf_aplic = df_country_graf[df_country_graf["Country"].isin(seleciona_pais_df_country)]
# st.line_chart(data=df_country_graf_aplic,
#               x="dt",
#               x_label="Data", 
#               y="AverageTemperature", 
#               y_label="Média de Temperadtura",
#               color="Country")
