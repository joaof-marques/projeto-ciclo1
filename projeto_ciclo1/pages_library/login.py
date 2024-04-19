import streamlit as st
import streamlit_authenticator as stauth
from controllers.system_log_controllers import insert_system_log
from streamlit_option_menu import option_menu
from pages_library.home import home
from pages_library.doc_page import doc_page
from pages_library.profile_page import profile_page
from pages_library.register_user_page import register_page
from pages_library.log_user_history import log_history
from pages_library.utils import fetch_users
from pages_library.utils import get_user_profile
from pages_library.login_functions import display_menu, display_menu_adm


def store_logged_user_credentials(username):
    _, credentials = get_user_profile(username)

    st.session_state.user_id = credentials['id']
    st.session_state.user_name = credentials['name']
    st.session_state.user_cpf = credentials['cpf']
    st.session_state.user_email = credentials['email']
    st.session_state.user_access_level = credentials['access_level']


def app():
    try:
        _, users = fetch_users()
        emails = []
        usernames = []
        passwords = []
        for user in users:
            emails.append(user['email'])
            usernames.append(user['username'])
            passwords.append(user['password'])

        
        credentials = {'usernames': {}}

        for index in range(len(emails)):
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
                    logout_button = Authenticator.logout(button_name='Sair', location='sidebar')
                    if logout_button:
                        clear_stored_user_credentials()
                    
                else:
                    st.warning('Usuario não existe')


    except Exception as error:
        st.warning(f'{error}')
        insert_system_log(error)
