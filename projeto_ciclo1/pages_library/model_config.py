import streamlit as st
from PIL import Image
import numpy as np
from projeto_ciclo1.database.database import *
import sparrow as spr

def model_config():
    try:
      
        title = st.text_input("Nome do modelo", key='model_name')
        uploaded_file = st.file_uploader("Selecione um arquivo", type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'])

        if uploaded_file is not None:

            spr.run(uploaded_file, title)  
            
    except Exception as e:
        print(e)
