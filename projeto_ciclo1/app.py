from pages_library.login import Login
import streamlit as st

st.set_page_config(page_title='RADE', page_icon='imgs/logo-rade.png', layout='wide')

Login.run()