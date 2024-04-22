import streamlit as st
from streamlit_option_menu import option_menu
from pages_library.home import home
from pages_library.doc_page import DocPage
from pages_library.profile_page import profile_page
from pages_library.register_user_page import register_page
from pages_library.log_user_history import log_history


def display_menu():
    with st.sidebar:          
        selected = option_menu(None, ["Início", "Documentos", "Perfil"], 
            icons=['house', 'cloud-upload', "list-task", 'gear'], 
            menu_icon="cast", default_index=0, orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color": "#ffff"},
                "icon": {"color": "#282634", "font-size": "14px"}, 
                "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#bd928b"},
                "nav-link-selected": {"background-color": "#ff4e44"},
            }
        )
    
    if selected == 'Início':
        home()

    if selected == 'Documentos':
        DocPage.draw()

    if selected == 'Perfil':
        profile_page()

def display_menu_adm():
    with st.sidebar:          
        selected = option_menu(None, ["Início", "Documentos", "Perfil", 'Cadastro', 'Logs'], 
                               icons=['house', 'file-earmark-text',
                                      "list-task", 'gear'],
            menu_icon="cast", default_index=0, orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color": "#ffff"},
                "icon": {"color": "#282634", "font-size": "14px"}, 
                "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#bd928b"},
                "nav-link-selected": {"background-color": "#ff4e44"},
            }
        )
    
    if selected == 'Início':
        home()

    if selected == 'Documentos':
        DocPage.draw()

    if selected == 'Perfil':
        profile_page()

    if selected == 'Cadastro':
        register_page()

    if selected == 'Logs':
        log_history()

