import streamlit as st
import streamlit_authenticator as stauth
from projeto_ciclo1.controllers.system_log_controllers import insert_system_log
from pages_library.utils import fetch_users
from pages_library.utils import get_user_profile
from pages_library.login_functions import display_menu, display_menu_adm


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
        
        credentials = {'usernames': {}}
        
        for index, user in enumerate(users):
            emails.append(user['email'])
            usernames.append(user['username'])
            passwords.append(user['password'])
            credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

        Authenticator = stauth.Authenticate(credentials, cookie_name='StreamLit', cookie_key='abcdef', cookie_expiry_days=0)

        email, authentication_status, username = Authenticator.login(fields={'Form name':'Entrar', 'Username':'Usuário', 'Password':'Senha', 'Login':'Entrar'})

        if username:
            if username in usernames:
                if authentication_status:
                    store_logged_user_credentials(username)

                    if st.session_state.user_access_level < 4:
                        display_menu()
                    else:
                        display_menu_adm()
                    Authenticator.logout(button_name='Sair', location='sidebar')

                else:
                    st.warning('Usuario não existe')

    except Exception as error:
        st.warning(f'{error}')
        insert_system_log(error)
