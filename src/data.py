# Importa bibliotecas
import streamlit as st
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
from datetime import date

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
# Cria e ajusta os dataframes
df_country = pd.read_csv(
    file_path_country,
    dtype={
        "AverageTemperature": float,
        "AverageTemperatureUncertainty": float,
        "Country": str
    },
    parse_dates=["dt"]
)
df_country["dt"] = pd.to_datetime(df_country["dt"])
df_country = df_country[df_country["dt"] >= "2000-01-01"].reset_index(drop=True)
df_country["dt"] = df_country["dt"].dt.date
# ----------------------------------------------------
df_state = pd.read_csv(
    file_path_state,
        dtype={
        "AverageTemperature": float,
        "AverageTemperatureUncertainty": float,
        "State": str,
        "Country": str
    },
    parse_dates=["dt"]
)
df_state["dt"] = pd.to_datetime(df_state["dt"])
df_state = df_state[df_state["dt"] >= "2000-01-01"].reset_index(drop=True)
df_state["dt"] = df_state["dt"].dt.date
# ----------------------------------------------------
df_temp = pd.read_csv(
    file_path_temp,
        dtype={
        "LandAverageTemperature": float,
        "LandAverageTemperatureUncertainty": float,
        "LandMaxTemperature": float,
        "LandMaxTemperatureUncertainty": float,
        "LandMinTemperature": float,
        "LandMinTemperatureUncertainty": float,
        "LandAndOceanAverageTemperature": float,
        "LandAndOceanAverageTemperatureUncertainty": float
    },
    parse_dates=["dt"]    
)
df_temp["dt"] = pd.to_datetime(df_temp["dt"])
df_temp = df_temp[df_temp["dt"] >= "2000-01-01"].reset_index(drop=True)
df_temp["dt"] = df_temp["dt"].dt.date