import streamlit as st
from data.processed import coletar_texto

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




# 6. Exibe o conteúdo na nova página do Streamlit.
st.title("Calor Intenso")
st.markdown(f"Fonte: [Blog da Raia](https://www.drogaraia.com.br/blog/saude/longevidade/calor-intenso)")

texto_reportagem = coletar_texto()
st.text(texto_reportagem)
