import requests
import streamlit as st
from bs4 import BeautifulSoup

# Configura o layout do streamlit
st.set_page_config(layout= 'wide') 

st.title("Consquências das Altas Temperaturas")
st.markdown("""
            O calor intenso pode ter efeitos significativos na saúde humana, especialmente em populações vulneráveis. A exposição prolongada a altas temperaturas pode levar a problemas 
            de saúde, incluindo desidratação, insolação e agravamento de condições médicas preexistentes. É essencial adotar medidas preventivas, como manter-se hidratado, evitar atividades 
            físicas extenuantes durante os períodos mais quentes do dia e buscar ambientes frescos sempre que possível.

            Vejamos a seguir uma reportabem do Blog da Raia que aborda os efeitos do calor intenso na saúde e fornece orientações sobre como se proteger durante ondas de calor.
            """
)            

# Endereço da reportagem.
URL = "https://www.drogaraia.com.br/blog/saude/longevidade/calor-intenso"

@st.cache_data
def coletar_texto(url):
    resposta = requests.get(url, timeout=30)
    resposta.raise_for_status()
    soup = BeautifulSoup(resposta.content, "html.parser")

    # 3. Seleciona a quarta div filha direta de blog-posting.
    # Equivale ao XPath: //*[@id="blog-posting"]/div[4]
    conteudo = soup.select_one("#blog-posting > div:nth-of-type(4)")

    for elemento in conteudo.select("script, style"):
        elemento.decompose()

    texto = conteudo.get_text(separator="\n", strip=True)

    return texto


# 6. Exibe o conteúdo na nova página do Streamlit.
st.title("Calor Intenso")
st.markdown(f"Fonte: [Blog da Raia]({URL})")

texto_reportagem = coletar_texto(URL)
st.text(texto_reportagem)
