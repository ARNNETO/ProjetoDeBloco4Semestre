import streamlit as st
from pathlib import Path
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
st.title("Tire Sua Dúvida")
st.markdown("""
            Aqui é seu espaço para que você possa tirar suas dúvidas sobre o aquecimento global e as mudanças climáticas.
            Sinta-se à vontade para enviar suas perguntas e você receberá respostas detalhadas e informativas.
            """)

image_path = (
    Path(__file__).resolve().parent.parent
    / "util"
    / "images"
    / "under_construction.png"
)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image(image_path)