from streamlit_option_menu import option_menu
from projeto_ciclo1.pages_library.home import home
from projeto_ciclo1.pages_library.doc_page import doc_page
from projeto_ciclo1.pages_library.profile_page import profile_page
from projeto_ciclo1.pages_library.register_user_page import register_page

# Horizontal menu
selected = option_menu(None, ["Início", "Documentos", "Perfil", 'Cadastro'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
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
    doc_page()

if selected == 'Perfil':
    profile_page()

if selected == 'Cadastro':
    register_page()
