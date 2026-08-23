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
