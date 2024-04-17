import streamlit as st
import streamlit_authenticator as stauth
from controllers.system_log_controllers import insert_system_log
from streamlit_option_menu import option_menu
from pages_library.home import home
from pages_library.doc_page import doc_page
from pages_library.profile_page import profile_page
from pages_library.register_user_page import register_page
from pages_library.fetch_users import fetch_users
from pages_library.utils import get_user_profile


def store_logged_user_credentials(username):
    _, credentials = get_user_profile(username)
    if 'user_id' not in st.session_state:
        st.session_state.user_id = credentials['id']
    if 'user_name' not in st.session_state:
        st.session_state.user_name = credentials['name']
    if 'user_cpf' not in st.session_state:
        st.session_state.user_cpf = credentials['cpf']
    if 'user_email' not in st.session_state:
        st.session_state.user_email = credentials['email']
    if 'user_access_level' not in st.session_state:
        st.session_state.user_access_level = credentials['access_level']


def app():
    try:
        _, users = fetch_users()
        emails = []
        usernames = []
        passwords = []
        for user in users:
            emails.append(user.email)
            usernames.append(user.username)
            passwords.append(user.password)

        
        credentials = {'usernames': {}}

        for index in range(len(emails)):
            credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
        
        Authenticator = stauth.Authenticate(credentials, cookie_name='StreamLit', cookie_key='abcdef', cookie_expiry_days=0)


        email, authentication_status, username = Authenticator.login(fields={'Form name':'Entrar', 'Username':'Usuário', 'Password':'Senha', 'Login':'Entrar'})
        store_logged_user_credentials(username)

        if username:
            if username in usernames:
                if authentication_status:
                    with st.sidebar:          
                        selected = option_menu(None, ["Início", "Documentos", "Perfil", 'Cadastro'], 
                            icons=['house', 'cloud-upload', "list-task", 'gear'], 
                            menu_icon="cast", default_index=0, orientation="vertical",
                            styles={
                                "container": {"padding": "0!important", "background-color": "#ffff"},
                                "icon": {"color": "#282634", "font-size": "14px"}, 
                                "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#bd928b"},
                                "nav-link-selected": {"background-color": "#ff4e44"},
                            }
                        )
                        Authenticator.logout(button_name='Sair', location='sidebar')

                    if selected == 'Início':
                        home()

                    if selected == 'Documentos':
                        doc_page()

                    if selected == 'Perfil':
                        profile_page()

                    if selected == 'Cadastro':
                        register_page()

                        
                else:
                    st.warning('Usuario não existe')


    except Exception as error:
        st.warning(f'{error}')
        insert_system_log(error)
