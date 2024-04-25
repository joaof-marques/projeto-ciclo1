import streamlit as st
from controllers.utils import validate_cpf, validate_email, validate_username, get_user_emails, get_usernames, update_password, delete_user, validate_name
from controllers.user_controllers import UserControllers
from streamlit_option_menu import option_menu
from controllers.logs_controllers import Log

class RegisterPage:
    @classmethod
    def register_store_user_credentials(self):
        if 'create_name' not in st.session_state:
            st.session_state.create_name = st.session_state.create_user_name
        if 'create_username' not in st.session_state:
            st.session_state.create_username = st.session_state.create_user_username
        if 'create_email' not in st.session_state:
            st.session_state.create_email = st.session_state.create_user_email
        if 'create_cpf' not in st.session_state:
            st.session_state.create_cpf = st.session_state.create_user_cpf
        if 'create_password' not in st.session_state:
            st.session_state.create_password = st.session_state.create_user_password
        if 'create_confirm_password' not in st.session_state:
            st.session_state.create_confirm_password = st.session_state.create_user_confirm_password
        if 'create_access_level' not in st.session_state:
            st.session_state.create_access_level = st.session_state.create_user_access_level

    @classmethod
    def delete_store_user_credentials(self):
                if 'delete_email' not in st.session_state:
                    st.session_state.delete_email = st.session_state.email_delete_user
                if 'delete_cpf' not in st.session_state:
                    st.session_state.delete_cpf = st.session_state.cpf_delete_user


    @classmethod
    def register_page(self):
        
        clm1, clm2, clm3 = st.columns([1, 3, 1])

        with clm2:
            clm1, clm2, clm3 = st.columns([2, 1, 2])
            with clm2:
                
                st.title('Cadastro')
        
            selected = option_menu(None, ['Cadastrar', 'Deletar'],
                                   icons=['person-add', 'trash'],
                                menu_icon="cast", default_index=0, orientation="horizontal",
                                styles={
                "container": {"padding": "0!important", "background-color": "#ffff"},
                "icon": {"color": "#282634", "font-size": "14px"},
                "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#bd928b"},
                "nav-link-selected": {"background-color": "#ff4e44"},
            }
            )

        if selected == 'Cadastrar':
            self.register_tab()
            
        if selected == 'Deletar':
            self.delete_tab()

    @classmethod
    def delete_tab(self):
        with st.form(key='delete_user', clear_on_submit=True):

            email = st.text_input(
                'Email', placeholder='Insira o email', key='email_delete_user')
            cpf = st.text_input(
                'CPF', placeholder='Insira o CPF', key='cpf_delete_user')

            delete_user_button = st.form_submit_button(
                'Excluir', type='primary', on_click=RegisterPage.delete_store_user_credentials)

            if delete_user_button:
                delete_user(email, cpf, st.session_state.user_id)
                st.success('Funcionário excluido com sucesso!')

    @classmethod
    def register_tab(self):
        try:
            with st.form(key='signup', clear_on_submit=True):
                name = st.text_input(
                    'Nome', key='create_user_name', placeholder='Nome')
                username = st.text_input(
                    'Usuario', key='create_user_username', placeholder='Nome de usuario')
                email = st.text_input(
                    'Email', key='create_user_email', placeholder='Email')
                cpf = st.text_input(
                    'CPF', key='create_user_cpf', placeholder='CPF')
                password = st.text_input(
                    'Senha', key='create_user_password', placeholder='Senha', type='password')
                confirm_password = st.text_input(
                    'Confirmar Senha', key='create_user_confirm_password', placeholder='Confirmar Senha', type='password')

                access_level = st.number_input(
                        'Nivel de Acesso', key='create_user_access_level', min_value=1, max_value=2, step=1)
                warning = st.empty()

                create_user_button = st.form_submit_button(
                        'Enviar', type='primary', on_click=self.register_store_user_credentials)

                if create_user_button:
                    if not username or len(username) < 4:
                        warning.warning(
                            'Nome de usuário inválido. Tamanho mínimo requerido: 4 caracteres')
                        return
                    if not validate_username(username):
                        warning.warning(
                            'Caracteres não suportados no nome do usuário.')
                        return
                    if not validate_name(name):
                        warning.warning('Digite um nome válido')
                        return
                    if not email:
                        warning.warning('Email inválido.')
                        return
                    if email in get_user_emails():
                        warning.warning('Email já registrado.')
                        return
                    if not validate_cpf(cpf):
                        warning.warning('CPF inválido.')
                        return
                    if len(password) < 8:
                        warning.warning(
                            'Senha muito curta. Tamanho mínimo requerido: 8 caracteres.')
                        return
                    if password != confirm_password:
                        warning.warning('Senhas não coincidem.')
                        return
                    UserControllers.create_user(name, username, email, cpf, password, access_level, st.session_state.user_id)
                    warning.empty()

                    st.success('Usuario criado')
                    return True
        except Exception as error:
            Log.insert_system_log(error)
            print(error)
            return False
