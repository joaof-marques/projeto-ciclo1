from pages_library.login import Login
import streamlit as st

st.set_page_config(page_title='RADE', page_icon='pages_library/icons/logo-rade.png', layout='wide')

Login.run()

# streamlit run projeto_ciclo1\app.py