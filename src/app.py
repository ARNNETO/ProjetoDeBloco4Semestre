# Importa bibliotecas
import streamlit as st
from pathlib import Path
from data import df_country, df_state, df_global, df_clima
import pandas as pd
import altair as alt

# Configura o layout do streamlit
st.set_page_config(layout= 'wide')

#=============================== FUNÇÕES
# Cria lista
@st.cache_data
def lista_opcoes(dataframe_lista: pd.DataFrame,
                 coluna: str) -> list:
    return sorted(dataframe_lista[coluna].unique().tolist())
# ------------------------------------------------
# Adiciona coluna ano
@st.cache_data
def col_ano(
    dataframe_ano: pd.DataFrame,
    coluna_ano: str
) -> pd.DataFrame:
    new_dataframe = dataframe_ano.copy()
    new_dataframe["ano"] = new_dataframe[coluna_ano].apply(
        lambda data: data.year
    )
    return new_dataframe

# ------------------------------------------------
# Baixa arquivos em csv
def baixar_arquivo(dataframe: pd.DataFrame, nome_do_arquivo: str):
    st.download_button(
        label="Baixar CSV",
        data=dataframe.to_csv(index=False).encode("utf-8"),
        file_name=nome_do_arquivo,
        mime="text/csv",
        key=f"download_{nome_do_arquivo}"
    )

#=============================== SESSION STATE
# Inicia as preferências antes de criar o session state
if 'cor_fundo' not in st.session_state:
    st.session_state.cor_fundo = '#FFFFFF'
# ------------------------------------------------
if 'cor_fonte' not in st.session_state:
    st.session_state.cor_fonte = '#000000'

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
df_global_ano = col_ano(df_global,"dt")

#=============================== SIDEBAR
st.sidebar.header("Filtros")
with st.sidebar:
    # Filtro de paises
    seleciona_pais = st.multiselect(
        "Por país",
        options=lista_opcoes(df_country, "Country"),
        default=["Brazil"],
        key="seleciona_pais"
    )

    df_state_por_pais = df_state[
    df_state["Country"].isin(seleciona_pais)
]
    estados_disponiveis = lista_opcoes(df_state_por_pais, "State")
    default_estado = ["Distrito Federal"] if "Distrito Federal" in estados_disponiveis else []

    seleciona_estado = st.multiselect(
        "Por estado",
        options=estados_disponiveis,
        default=default_estado,
        key="seleciona_estado"
    )

    # Filtro ano
    seleciona_ano = st.multiselect(
        "Por ano",
        options=lista_opcoes(df_global_ano, "ano"), 
        default=[2000],
        key="seleciona_ano"
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
st.write("Clique no botão abaixo para baixar os dados filtrados :arrow_down_small::")
baixar_arquivo(df_state_filtrado,"temperatura_por_pais")
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
baixar_arquivo(df_state_filtrado,"temperatura_por_estado")
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
baixar_arquivo(df_global_filtrado,"temperatura_global")
st.markdown("---")
# ------------------------------------------------

st.subheader("Temperadura em São Paulo", text_alignment="center")
st.text("São Paulo já foi considerada a terra da garoa. Em dias de frio eram tensos. O calor não castigava tanto. Hoje, por conta do aquecimento global, o cenário é outros.")
st.text("Vejamos a seguir a métia de temperatura entre os anos de 1991-2020 conforme o Wikipedia")
st.dataframe(df_clima)
st.markdown("---")

# ------------------------------------------------
st.header("Continuação Das Observações", text_alignment="center")
st.text("Você pode agregar outras fontes de informação para compara-las com as já exibidas anteriormente.")
recebe_arquivo = st.file_uploader("Faça o upload de um arquivo csv", type=["csv"])
if recebe_arquivo is not None:
    df_upload = pd.read_csv(recebe_arquivo, dtype=str)
    st.dataframe(df_upload)
else:
    st.info("Faça o upload de um arquivo CSV para visualizar os dados abaixo.")
    