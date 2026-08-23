# Importa bibliotecas
import streamlit as st
from pathlib import Path
from data import df_country, df_state, df_temp

# Configura o layout do streamlit
st.set_page_config(layout= 'wide')

# Diretório para coletar os arquivos 
root_dir = Path(__file__).parent.parent
print(root_dir)

#=============================== VISUALIZAÇÕES
# Exibe amostra dos dataframes
st.title('Monitoramento da Temperatura Global :fire_extinguisher: :fire:')
st.image(root_dir/'util/images/aquecimento-global.jpg',caption='"Quanto mais demorarmos para reduzir as emissões, mais caro vai custar para mantermos o aumento da temperatura em 2ºC". - Rajendra Pachauri, presidente IPCC',width=300)
st.subheader('Este painel tem como objetivo monitar o aquecimento global, ajudando na tomada de desição de forma rápida e segura.')
st.write('Você pode conferir a fonte dos dados no link https://www.kaggle.com/datasets/sachinsarkar/climate-change-global-temperature-data')
st.write('Você também pode se aprofundar nos Objetivos de Desenvolvimento Sustentavel acessando o link https://conectabrasil.org/home')
st.write('Amostra do dataset GlobalLandTemperaturesByCountry')
st.dataframe(df_country.head(10))
st.write('Amostra do dataset GlobalLandTemperaturesByState')
st.dataframe(df_state.head(10))
st.write('Amostra do dataset GlobalLandTemperatures')
st.dataframe(df_temp.head(10))
