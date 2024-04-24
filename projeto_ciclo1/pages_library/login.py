import streamlit as st
import streamlit_javascript as st_js
from controllers.logs_controllers import Log
from controllers.utils import get_user_profile
from streamlit_option_menu import option_menu
from sqlalchemy.orm import Session
from database.database import User, engine
from pages_library.home import Home
from pages_library.doc_page import DocPage
from pages_library.profile_page import ProfilePage
from pages_library.register_user_page import RegisterPage
from pages_library.log_user_history import LogHistory
import os
import bcrypt
import re


class Login:
    
    @classmethod
    def run(self):
        
        
        col1, col2, col3 = st.columns(3)
        with col2:
                
            if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
                col1, col2, col3 = st.columns([1, 10, 1])
                with col2:

                    theme = st_js.st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")
                    if theme == 'dark':
                        image_path = os.path.join(os.path.dirname(__file__), r'Icons', r'light.png')
                    else:
                        image_path = os.path.join(os.path.dirname(__file__), r'Icons', r'dark.png')
                    st.image(image_path)
                    
                self.authentication_handler()
                login_form = st.form('Entrar', clear_on_submit=True)
                login_form = st.form('Login', clear_on_submit=True)
                login_form.subheader('Entrar')
                username = login_form.text_input('Usuário', key='user')
                password = login_form.text_input(
                    'Senha', type='password', key='pw')

                if login_form.form_submit_button('Entrar', on_click=self.store_user_login_credentials):
                    if self.login_fetch_user(username, password):
                        self.store_logged_user_credentials(username)
                        self.execute_login()

                    else:
                        st.error('Credenciais inválidas. Tente novamente.')
        if st.session_state.authentication_status:

            if st.session_state.user_access_level < 2:
                self.display_menu()
            else:
                self.display_menu_adm()

                
    @classmethod
    def authentication_handler(self):
        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None

            
    @classmethod
    def store_user_login_credentials(self):
        st.session_state.username = st.session_state.user

        
    @classmethod
    def login_fetch_user(self, username, password):
        try:

            with Session(bind=engine) as session:

                user = session.query(User).filter_by(username=username).first()

                if user.deleted == True:
                    return False
                if not self.is_hash(password):

                    if user.username == username and user.password == password:
                        return True

                if user.username == username and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

                    return True

                return False
        except Exception as err:

            return False

    @classmethod
    def store_logged_user_credentials(self, username):
        _, credentials = get_user_profile(username)
        st.session_state.user_id = credentials['id']
        st.session_state.user_name = credentials['name']
        st.session_state.user_cpf = credentials['cpf']
        st.session_state.user_email = credentials['email']
        st.session_state.user_access_level = credentials['access_level']

        
    @classmethod
    def execute_login(self):
        st.session_state['logout'] = False
        st.session_state['authentication_status'] = True
        st.rerun()

        
    @classmethod
    def is_hash(self, hash_string):
        bcrypt_regex = re.compile(r'^\$2[aby]\$\d+\$.{53}$')
        return bool(bcrypt_regex.match(hash_string))

      
    @classmethod
    def execute_logout(self):
        st.session_state['logout'] = True
        st.session_state['authentication_status'] = None


    @classmethod
    def display_menu(self):
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
            col1, col2, col3 = st.columns(3)
            with col2:
                st.button('Sair', on_click=self.execute_logout)
        
        if selected == 'Início':
            Home.home()

        if selected == 'Documentos':
            DocPage.doc_page()

        if selected == 'Perfil':
            ProfilePage.profile_page()

    @classmethod
    def display_menu_adm(self):
        with st.sidebar:          
            selected = option_menu(None, ["Início", "Documentos", "Perfil", 'Cadastro', 'Logs'], 
                                   icons=['house', 'cloud-upload',
                                          "list-task", 'gear', 'code-square'],
                menu_icon="cast", default_index=0, orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "#ffff"},
                    "icon": {"color": "#282634", "font-size": "14px"}, 
                    "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#bd928b"},
                    "nav-link-selected": {"background-color": "#ff4e44"},
                }
            )
            col1, col2, col3 = st.columns(3)
            with col2:
                st.button('Sair', on_click=self.execute_logout)
            
        if selected == 'Início':
            Home.home()

        if selected == 'Documentos':
            DocPage.doc_page()

        if selected == 'Perfil':
            ProfilePage.profile_page()

        if selected == 'Cadastro':
            RegisterPage.register_page()

        if selected == 'Logs':
            LogHistory.log_history()

