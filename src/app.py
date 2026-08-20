# Importa bibliotecas
import streamlit as st
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path

# Inicia a API
api = KaggleApi()
api.authenticate()

# Diretório onde o dataset será baixado e descompactado
dataset_dir = 'data/'

# Diretório para coletar os arquivos 
root_dir = Path(__file__).parent.parent
print(root_dir)

# Baixa os arquivos
api.dataset_download_files('sachinsarkar/climate-change-global-temperature-data', path=dataset_dir, unzip=True)

## Coleta caminho dos arquivos
file_path_country = root_dir/'data/datasets/GlobalLandTemperaturesByCountry.csv'
file_path_state = root_dir/'data/datasets/GlobalLandTemperaturesByState.csv'
file_path_temp= root_dir/'data/datasets/GlobalTemperatures.csv'

#=============================== DATAFRAMES
# Cria os dataframes
df_country = pd.read_csv(file_path_country)
df_state = pd.read_csv(file_path_state)
df_temp = pd.read_csv(file_path_temp)


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
