from pages_library.login import Login
import streamlit as st
import os

st.set_page_config(page_title='RADE', page_icon=os.path.join(os.path.dirname(__file__), r'pages_library', r'icons', r'logo-rade.png'), layout='wide')

Login.run()

# streamlit run projeto_ciclo1\app.py