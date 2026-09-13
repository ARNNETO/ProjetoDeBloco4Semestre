import requests
import pandas as pd
from bs4 import BeautifulSoup

url = (
    "https://pt.wikipedia.org/wiki/"
    "Clima_da_cidade_de_S%C3%A3o_Paulo"
)

# Identifica o programa que está fazendo a requisição
AGENTE = "INFNET - Proj Bloco (trabalho escolar sobre ODS 13)"


# Faz a requisição para a página
response = requests.get(
    url,
    headers={"User-Agent":AGENTE},
    timeout=30
)

# Interrompe o código caso a requisição apresente erro
response.raise_for_status()

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

print(cabecalhos)

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

print(df_clima.head())



