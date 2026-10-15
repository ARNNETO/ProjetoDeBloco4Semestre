import requests
import streamlit as st
from bs4 import BeautifulSoup

# Configura o layout do streamlit
st.set_page_config(layout= 'wide') 

# Endereço da reportagem.
URL = "https://www.drogaraia.com.br/blog/saude/longevidade/calor-intenso"

@st.cache_data
def coletar_texto(url):
    # 1. Faz a requisição para obter o HTML da página.
    # O timeout limita o tempo de espera pela resposta.
    resposta = requests.get(url, timeout=30)

    # Interrompe a coleta caso o site retorne um erro HTTP.
    resposta.raise_for_status()

    # 2. Converte o HTML em um objeto Beautiful Soup.
    soup = BeautifulSoup(resposta.content, "html.parser")

    # 3. Seleciona a quarta div filha direta de blog-posting.
    # Equivale ao XPath: //*[@id="blog-posting"]/div[4]
    conteudo = soup.select_one("#blog-posting > div:nth-of-type(4)")

    # Verifica se o elemento existe no HTML recebido.
    if conteudo is None:
        raise ValueError("O bloco de texto não foi encontrado no HTML recebido.")

    # 4. Remove elementos que não fazem parte do texto da reportagem.
    for elemento in conteudo.select("script, style"):
        elemento.decompose()

    # 5. Extrai todo o texto do bloco, sem resumir ou cortar.
    texto = conteudo.get_text(separator="\n", strip=True)

    if not texto:
        raise ValueError("O bloco encontrado está vazio.")

    return texto


# 6. Exibe o conteúdo na nova página do Streamlit.
st.title("Calor intenso")
st.markdown(f"Fonte: [Blog da Raia]({URL})")

try:
    texto_reportagem = coletar_texto(URL)
    st.text(texto_reportagem)

except requests.exceptions.RequestException as erro:
    st.error(f"Não foi possível acessar a reportagem: {erro}")

except ValueError as erro:
    st.error(str(erro))