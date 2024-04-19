import streamlit as st
from controllers.utils import validate_cpf, validate_email, validate_username, get_user_emails, get_usernames, update_password, delete_user, validate_name
from controllers.user_controllers import create_user

def register_store_user_credentials():
    if 'name' not in st.session_state:
         st.session_state.name = st.session_state.create_user_name
    if 'username' not in st.session_state:
        st.session_state.username = st.session_state.create_user_username
    if 'email' not in st.session_state:
        st.session_state.email = st.session_state.create_user_email
    if 'cpf' not in st.session_state:
        st.session_state.cpf = st.session_state.create_user_cpf
    if 'password' not in st.session_state:
        st.session_state.password = st.session_state.create_user_password
    if 'access_level' not in st.session_state:
        st.session_state.access_level = st.session_state.create_user_access_level


def delete_store_user_credentials():
            if 'email' not in st.session_state:
                st.session_state.email = st.session_state.email_delete_user
            if 'cpf' not in st.session_state:
                st.session_state.cpf = st.session_state.cpf_delete_user

def register_page():
    st.subheader('Cadastro de funcionário:')

    tab_register, tab_delete_user = st.tabs(['Cadastrar', 'Deletar'])

    

    with tab_register:

            with st.form(key='signup', clear_on_submit=True):
                # st.subheader(':red[Cadastro]')
                name = st.text_input('Nome', key='create_user_name', placeholder='Nome')
                username = st.text_input('Usuario', key='create_user_username', placeholder='Nome de usuario')
                email = st.text_input('Email', key='create_user_email', placeholder='Email')
                cpf = st.text_input('CPF', key='create_user_cpf', placeholder='CPF')
                password = st.text_input('Senha', key='create_user_password', placeholder='Senha', type='password')
                confirm_password = st.text_input('Confirmar Senha', key='create_user_confirm_password', placeholder='Confirmar Senha', type='password')
                
                access_level = st.number_input('Nivel de Acesso', key='create_user_access_level', min_value=1, max_value=4, step=1)
                warning = st.empty()

                create_user_button = st.form_submit_button('Enviar', type='primary', on_click=register_store_user_credentials)

                if create_user_button:
                    if not username or len(username) < 4:
                        warning.warning('Nome de usuário inválido. Tamanho mínimo requerido: 4 caracteres')
                        return
                    if not validate_username(username):
                        warning.warning('Caracteres não suportados no nome do usuário.')
                        return
                    if not validate_name(name):
                        warning.warning('Digite um nome válido')
                    if not email:
                        warning.warning('Email inválido.')
                        return
                    if email in get_user_emails():
                        warning.warning('Email já registrado.')
                        return
                    if not validate_cpf(cpf):
                        warning.warning('CPF inválido.')
                        return
                    if len(password)<8:
                        warning.warning('Senha muito curta. Tamanho mínimo requerido: 8 caracteres.')
                        return
                    if st.session_state.password != confirm_password:
                         warning.warning('Senhas não coincidem.')
                         return
                    
                    create_user(name, username, email, cpf, password, access_level, st.session_state.user_id)
                    warning.empty()
                    st.success('Usuario criado')
                    return True


    with tab_delete_user:
        with st.form(key='delete_user', clear_on_submit=True):
        
            email = st.text_input('Email', placeholder='Insira o email', key='email_delete_user')
            cpf = st.text_input('CPF', placeholder='Insira o CPF', key='cpf_delete_user')


            delete_user_button = st.form_submit_button('Excluir', type='primary', on_click=delete_store_user_credentials)

            if delete_user_button:
                delete_user(email, cpf)
                st.success('Funcionário excluido com sucesso!')

