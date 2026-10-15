# Importa bibliotecas
import streamlit as st
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
from datetime import date
import requests
from bs4 import BeautifulSoup


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
df_global= pd.read_csv(
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
df_global["dt"] = pd.to_datetime(df_global["dt"])
df_global = df_global[df_global["dt"] >= "2000-01-01"].reset_index(drop=True)
df_global["dt"] = df_global["dt"].dt.date

#=============================== SCRAP

url = (
    "https://pt.wikipedia.org/wiki/"
    "Clima_da_cidade_de_S%C3%A3o_Paulo"
)

# Cria a identificação do agente
AGENTE = "INFNET - Proj Bloco (trabalho escolar sobre ODS 13)"


# Faz a requisição para a página
response = requests.get(
    url,
    headers={"User-Agent":AGENTE},
    timeout=30
)


# Converte o HTML para um objeto BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

tabela_clima = None

tabelas = soup.find_all("table")

for tabela in tabelas:
    texto_tabela = tabela.get_text(
        separator=" ",
        strip=True
    )

    if "Dados climatológicos para São Paulo" in texto_tabela:
        tabela_clima = tabela
        break

if tabela_clima is None:
    raise ValueError("A tabela climatológica não foi encontrada.")

# Localiza todas as linhas da tabela
linhas = tabela_clima.find_all("tr")

linha_cabecalho = None
indice_cabecalho = None

# Procura o cabeçalho verdadeiro
for indice, linha in enumerate(linhas):
    textos = [
        celula.get_text(" ", strip=True)
        for celula in linha.find_all(["th", "td"])
    ]

    if "Mês" in textos and any("Jan" in texto for texto in textos):
        linha_cabecalho = linha
        indice_cabecalho = indice
        break

if linha_cabecalho is None:
    raise ValueError("O cabeçalho da tabela não foi encontrado.")

cabecalhos = [
    celula.get_text(" ", strip=True)
    for celula in linha_cabecalho.find_all(["th", "td"])
]

dados = []

# Começa na linha seguinte ao cabeçalho
for linha in linhas[indice_cabecalho + 1:]:
    celulas = linha.find_all(["th", "td"])

    valores = [
        celula.get_text(" ", strip=True)
        for celula in celulas
    ]

    # Adiciona somente linhas com a mesma quantidade de colunas
    if len(valores) == len(cabecalhos):
        dados.append(valores)

df_clima = pd.DataFrame(
    dados,
    columns=cabecalhos
)