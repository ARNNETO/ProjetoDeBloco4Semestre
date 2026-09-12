# Importa bibliotecas
import streamlit as st
from pathlib import Path
from data import df_country, df_state, df_temp

# Configura o layout do streamlit
st.set_page_config(layout= 'wide')

#=============================== SESSION STATE
# Inicia as preferências antes de criar o session state
if 'cor_fundo' not in st.session_state:
    st.session_state.cor_fundo = '#FFFFFF'

if 'cor_fonte' not in st.session_state:
    st.session_state.cor_fonte = '#000000'

# Diretório para coletar os arquivos 
root_dir = Path(__file__).parent.parent
print(root_dir)

#=============================== CONFIGURAÇÃO DA PÁGINA

st.title('Monitoramento da Temperatura Global :fire_extinguisher: :fire:',text_alignment="center")
coltext1, coltext2, coltext3, coltext4 = st.columns((6,1,1,1))
with coltext1:
    st.image(root_dir/'util/images/aquecimento-global.jpg',caption='"Quanto mais demorarmos para reduzir as emissões, mais caro vai custar para mantermos o aumento da temperatura em 2ºC". - Rajendra Pachauri, presidente IPCC',width=300)
# with coltext2:
#     st.text("Configure as cores da página")
with coltext3:
    st.color_picker("Escolha a cor de fundo:", key="cor_fundo")
with coltext4:
    st.color_picker("Escolha a cor da fonte:", key="cor_fonte")


# # Seleção das cores
# col1, col2, col3 = st.columns((6,1,1))
# with col2:
#     st.color_picker("Escolha a cor de fundo:", key="cor_fundo")
# with col3:
#     st.color_picker("Escolha a cor da fonte:", key="cor_fonte")

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
# st.image(root_dir/'util/images/aquecimento-global.jpg',caption='"Quanto mais demorarmos para reduzir as emissões, mais caro vai custar para mantermos o aumento da temperatura em 2ºC". - Rajendra Pachauri, presidente IPCC',width=300)
st.subheader('Este painel tem como objetivo monitar o aquecimento global, ajudando na tomada de desição de forma rápida e segura.')
st.markdown('Você pode conferir a fonte dos dados [aqui.](https://www.kaggle.com/datasets/sachinsarkar/climate-change-global-temperature-data)')
st.markdown('Você também pode se aprofundar nos "Objetivos de Desenvolvimento Sustentavel" acessando o [link.](https://conectabrasil.org/home)')
st.write('Amostra do dataset GlobalLandTemperaturesByCountry')
st.dataframe(df_country.head(10))
st.write('Amostra do dataset GlobalLandTemperaturesByState')
st.dataframe(df_state.head(10))
st.write('Amostra do dataset GlobalLandTemperatures')
st.dataframe(df_temp.head(10))
