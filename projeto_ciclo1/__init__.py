import streamlit as st
from streamlit_option_menu import option_menu
from pages_library import doc_page, profile_page, register_user_page

# Horizontal menu
selected = option_menu(None, ["Início", "Documentos", "Perfil", 'Cadastro'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
if selected == 'Início':
    st.write('Início teste')

if selected == 'Documentos':
    doc_page.doc_page()

if selected == 'Perfil':
    profile_page.profile_page()

if selected == 'Cadastro':
    register_user_page.register_page()