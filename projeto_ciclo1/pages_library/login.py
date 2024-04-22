import streamlit as st
import streamlit_authenticator as stauth
from controllers.system_log_controllers import insert_system_log
from controllers.utils import fetch_users
from controllers.utils import get_user_profile
from pages_library.login_functions import display_menu, display_menu_adm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.database import User
engine = create_engine('postgresql+psycopg2://postgres:12345@localhost/desafio_name')
import bcrypt
import re

def is_hash(hash_string):

    bcrypt_regex = re.compile(r'^\$2[aby]\$\d+\$.{53}$')
    return bool(bcrypt_regex.match(hash_string))




def authentication_handler():
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'logout' not in st.session_state:
        st.session_state['logout'] = None

def store_user_login_credentials():
    st.session_state.username = st.session_state.user

def login_fetch_user(username, password):
    try:

        with Session(bind=engine) as session:

            user = session.query(User).filter_by(username = username).first()
            print('43')
            if user.deleted == True:
                return False
            if not is_hash(password):
                print('47')
                if user.username == username and user.password == password:
                    print('49')
                    return True
            if user.username == username and bcrypt.checkpw( password.encode('utf-8'), user.password.encode('utf-8')):
                print('52')
                return True
            print('54')
            return False
    except Exception as err:
        print('57', err)
        return False

def store_logged_user_credentials(username):
    _, credentials = get_user_profile(username)

    st.session_state.user_id = credentials['id']
    st.session_state.user_name = credentials['name']
    st.session_state.user_cpf = credentials['cpf']
    st.session_state.user_email = credentials['email']
    st.session_state.user_access_level = credentials['access_level']

def execute_login():
    st.session_state['logout'] = False
    st.session_state['authentication_status'] = True
    st.rerun()

def app():
    if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
        authentication_handler()
        login_form = st.form('Entrar', clear_on_submit=True)
        login_form = st.form('Login', clear_on_submit=True)
        login_form.subheader('Entrar')
        username = login_form.text_input('Usuário', key='user')
        password = login_form.text_input('Senha', type='password', key='pw')

  
        if login_form.form_submit_button('Entrar', on_click=store_user_login_credentials):
            if login_fetch_user(username, password):
                store_logged_user_credentials(username)
                execute_login()

            else:
                st.error('Credenciais inválidas. Tente novamente.')
    if st.session_state.authentication_status:

        if st.session_state.user_access_level < 4:
            display_menu()
        else:
            display_menu_adm()


# def app():
#     try:
#         _, users = fetch_users()
#         emails = []
#         usernames = []
#         passwords = []
#         credentials = {'usernames': {}}

#         for index, user in enumerate(users):
#             emails.append(user['email'])
#             usernames.append(user['username'])
#             passwords.append(user['password'])
#             credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

        

#         # for index in range(len(emails)):
#         #     credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
        
#         Authenticator = stauth.Authenticate(credentials, cookie_name='StreamLit', cookie_key='abcdef', cookie_expiry_days=0)


#         email, authentication_status, username = Authenticator.login(fields={'Form name':'Entrar', 'Username':'Usuário', 'Password':'Senha', 'Login':'Entrar'})

#         if username:
#             if username in usernames:
#                 if authentication_status:
#                     store_logged_user_credentials(username)

#                     if st.session_state.user_access_level < 4:
#                         display_menu()
#                     else:
#                         display_menu_adm()
#                     logout_button = Authenticator.logout(button_name='Sair', location='sidebar')

                    
#                 else:
#                     st.warning('Usuario não existe')


#     except Exception as error:
#         st.warning(f'{error}')
#         insert_system_log(error)
