# Importa bibliotecas
import streamlit as st
from pathlib import Path
from data import df_country, df_state, df_global, df_clima
from datetime import date
import pandas as pd
from matplotlib.pyplot import plot
import altair as alt

# Configura o layout do streamlit
st.set_page_config(layout= 'wide')

#=============================== FUNÇÕES
# Filtra país
# def filtra_dataframe_v2(
#     dataframe_pais: pd.DataFrame,
#     coluna: str,
#     dado_filtrado
# ) -> pd.DataFrame:
#     df_filtrado = dataframe_pais[
#         dataframe_pais[coluna].isin(dado_filtrado)
#     ]
#     return df_filtrado
# # ------------------------------------------------
# Cria lista de anos
# def lista_ano(dataframe_ano: pd.DataFrame) -> list:
#     return sorted(dataframe_ano["dt"].
#                   apply(lambda data: data.year)
#                   .unique()
#                   .tolist())
# ------------------------------------------------
# Cria lista
def lista_opcoes(dataframe_lista: pd.DataFrame,
                 coluna: str) -> list:
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
#=============================== LISTA DE FILTROS
# # Lista de país
# lista_opcoes_df_country = lista_opcoes(df_country,"Country")
# # Lista de estados
# lista_opcoes_df_state = lista_opcoes(df_state,"State")
# # Cria feature Ano e lista ano
df_global_ano = col_ano(df_global,"dt")
# lista_opcoes_ano = lista_opcoes(df_global_ano,"ano")

#=============================== SIDEBAR
st.sidebar.header("Filtros")
with st.sidebar:
    # Filtro de paises
    seleciona_pais = st.multiselect(
        "Por país",
        options=sorted(df_country["Country"].dropna().unique()),
        default=["Brazil"]
    )

    # Estados disponíveis com filtro por país
    estados_disponiveis = sorted(
        df_state[
            df_state["Country"].isin(seleciona_pais)
        ]["State"].dropna().unique()
    )

    seleciona_estado = st.multiselect(
        "Por estado",
        options=estados_disponiveis,
        default=["Distrito Federal"]
    )

    # Filtro ano
    seleciona_ano = st.multiselect(
        "Por ano",
        options=sorted(df_global_ano["ano"].unique()), 
        default=[2000]
    )
#=============================== APLICA OS FILTROS
df_country_filtrado = df_country[
    df_country["Country"].isin(seleciona_pais)
    ]
df_state_filtrado = df_state[
    (df_state["Country"].isin(seleciona_pais)) &
    (df_state["State"].isin(seleciona_estado))
]
df_global_filtrado = df_global_ano[
    df_global_ano["ano"].isin(seleciona_ano)
]

#=============================== VISUALIZAÇÕES
# Exibe apresentações
st.subheader('Este painel tem como objetivo monitorar o aquecimento global a partir do ano 2000, ajudando na tomada de decição de forma rápida e segura.')
st.markdown('Você pode conferir a fonte dos dados [aqui.](https://www.kaggle.com/datasets/sachinsarkar/climate-change-global-temperature-data)')
st.markdown('Você também pode se aprofundar nos "Objetivos de Desenvolvimento Sustentável" acessando o [link.](https://conectabrasil.org/home)')
st.markdown("---")
# ------------------------------------------------

# Exibe dados do dataframe df_country
st.subheader('Temperatura Média Por País',text_alignment="center")
# st.dataframe(df_country.head(10))
st.text("Para podermos entender como está a temperatura global, deve-se observar onde se concentra os maiores picos para que seja planejado a melhor estratégia de redução do aquecimento global seguindo obviamente a característica deste país.")
st.text("Vamos olhar os dados detalhados:")
st.dataframe(df_country_filtrado)
st.text("Vamos ver a média de temperatura por país selecionado")
line_chart_country = alt.Chart(df_country_filtrado).mark_line(interpolate='basis').encode(
    alt.X("dt:T", title='Data'),
    alt.Y('AverageTemperature:Q', title='Temperatura'),
    color=alt.Color("Country:N", title="País"),
            tooltip=[
            alt.Tooltip("dt:T", title="Data"),
            alt.Tooltip("AverageTemperature:Q", title="Temperatura"), 
            alt.Tooltip("Country:N", title="País")
        ]
).properties(
        title=alt.TitleParams(
            text="Temperatura Média Por País",
            anchor="middle"
        )
)
st.altair_chart(line_chart_country) 
st.markdown("---")
# ------------------------------------------------
 
# Exibe dados do dataframe df_state
st.subheader("Temperatura Média Por Estado",text_alignment="center")
st.text('Aqui podemos olhar como está a média de temperadora por cada estado.')
st.text("Vejamos abaixo:")
st.dataframe(df_state_filtrado)
st.text("Vamos ver a média de temperadora por país selecionado")
line_chart_state = alt.Chart(df_state_filtrado).mark_line(interpolate='basis').encode(
    alt.X("dt:T", title='Data'),
    alt.Y('AverageTemperature', title='Temperatura'),
    color=alt.Color("State:N", title="Estado"),
            tooltip=[
            alt.Tooltip("dt:T", title="Data"),
            alt.Tooltip("AverageTemperature:Q", title="Temperatura"), 
            alt.Tooltip("Country:N", title="País")
        ]
).properties(
        title=alt.TitleParams(
            text="Temperatura Média Por Estado",
            anchor="middle"
        )
)
st.altair_chart(line_chart_state)
st.markdown("---")
# ------------------------------------------------

# Exibe dados do dataframe df_global
st.subheader("Temperatura Média Global",text_alignment="center")
st.text("Vamos observar a temperatura Global")
st.dataframe(df_global_filtrado)
st.text("Podemos ver as temperaturas mínimas e máximas por ano selecionado")
line_chart_global = alt.Chart(df_global_filtrado).transform_fold(
    ["LandMaxTemperature", "LandMinTemperature"],
    as_=["Tipo de Temperatura", "Temperatura"]
).mark_line(interpolate='basis').encode(
    alt.X("dt:T", title="Data"),
    alt.Y("Temperatura:Q", title="Temperatura"),
    color=alt.Color(
        "Tipo de Temperatura:N", 
        title="Temperatura",
        legend=alt.Legend(
            labelExpr="datum.label == 'LandMaxTemperature' ? 'Máxima' : 'Mínima'"
    )
),
    tooltip=[
        alt.Tooltip("dt:T", title="Data"),
        alt.Tooltip("Tipo de Temperatura:N", title="Tipo"),
        alt.Tooltip("Temperatura:Q", title="Temperatura"),
        alt.Tooltip("ano:N", title="Ano")
    ]
).properties(
    title=alt.TitleParams(
        text="Temperatura Máxima e Mínima Global",
        anchor="middle"
    )
)
st.altair_chart(line_chart_global)
st.markdown("---")
# ------------------------------------------------

st.subheader("Temperadura em São Paulo", text_alignment="center")
st.text("São Paulo já foi considerada a terra da garoa. Em dias de frio eram tensos. O calor não castigava tanto. Hoje, por conta do aquecimento global, o cenário é outros.")
st.text("Vejamos a seguir a métia de temperatura entre os anos de 1991-2020 conforme o Wikipedia")
st.dataframe(df_clima)
