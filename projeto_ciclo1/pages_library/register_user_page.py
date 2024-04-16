import streamlit as st
from page.utils import validate_cpf, validate_email, validate_username, get_user_emails, get_usernames, update_password, update_email, delete_user
from controllers.user_controllers import create_user

def register_store_user_credentials():
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

def update_password_store_user_credentials():
        if 'email' not in st.session_state:
            st.session_state.email = st.session_state.email_user
        
        if 'password' not in st.session_state:
            st.session_state.password = st.session_state.update_password
        

def delete_store_user_credentials():
            if 'email' not in st.session_state:
                st.session_state.email = st.session_state.email_delete_user
            if 'cpf' not in st.session_state:
                st.session_state.cpf = st.session_state.cpf_delete_user

def register_page():
    st.subheader('Cadastro de funcionário:')

    tab_register, tab_update_password, tab_delete_user = st.tabs(['Cadastrar', 'Alterar Senha', 'Deletar'])

    

    with tab_register:
            

            with st.form(key='signup', clear_on_submit=True):
                st.subheader(':red[Cadastro]')
                username = st.text_input('Usuario', key='create_user_username', placeholder='Usuario')
                email = st.text_input('Email', key='create_user_email', placeholder='Email')
                cpf = st.text_input('CPF', key='create_user_cpf', placeholder='CPF')
                password = st.text_input('Senha', key='create_user_password', placeholder='Senha', type='password')
                access_level = st.number_input('Nivel de Acesso', key='create_user_access_level', min_value=1, max_value=4, step=1)
 
                
                if st.form_submit_button('Enviar', type='primary', on_click=register_store_user_credentials):
                    if not username or len(username) <= 4:
                        st.warning('Nome de usuário inválido. Tamanho mínimo requerido: 4 caracteres')
                        return
                    if not validate_username(username):
                        st.warning('Caracteres não suportados.')
                        return
                    if not email:
                        st.warning('Email inválido.')
                        return
                    if email in get_user_emails():
                        st.warning('Email já registrado.')
                        return
                    if not validate_cpf(cpf):
                        st.warning('CPF inválido.')
                        return
                    if len(password)<8:
                        st.warning('Senha muito curta. Tamanho mínimo requerido: 8 caracteres.')
                        return
                    
                    create_user(username, email, cpf, password, access_level)
                    st.success('Usuario criado')
                    return True

    with tab_update_password:
        team = st.selectbox(
            "Funcionários: ",
            ('Fulano', 'Ciclano', 'Beltrano', 'Tiago', 'Joãos', 'Feliphe'),
            index=None,
            placeholder="Selecione o funcionário"
            )
        
        st.divider()


                

        with st.form(key='change_email', clear_on_submit=True):
            email = st.text_input('E-mail:', placeholder='Email', key='email_user')
            new_password = st.text_input('Senha', placeholder='Insira nova senha', type='password', key='update_password')

            confirm_new_password = st.text_input('Senha', placeholder='Confirme a nova senha', type='password', key='confirm_update_password')
            

            if new_password != confirm_new_password and (not validate_email(email)):
                st.warning('Credenciais inválidas')
                return False                

            register_button = st.form_submit_button(label="Salvar", type='primary', on_click=update_password_store_user_credentials)
            if register_button:
                update_password(email, new_password)
                st.success('Senha de funcionário atualizado')

    with tab_delete_user:
        team = st.selectbox(
            'Funcionários: ', 
            ('Fulano', 'Ciclano', 'Beltrano', 'Tiago', 'Joãos', 'Feliphe'),
            placeholder="Selecione o funcionário"
            )

        
        email = st.text_input('Email', placeholder='Insira o email', key='email_delete_user')
        cpf = st.text_input('CPF', placeholder='Insira o CPF', key='cpf_delete_user')


        del_funcionário = st.button('Excluir', type='primary', on_click=delete_store_user_credentials)

        if del_funcionário:
            delete_user(email, cpf)
            st.success('Funcionário excluido com sucesso!')

