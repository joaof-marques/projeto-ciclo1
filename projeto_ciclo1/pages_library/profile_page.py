import streamlit as st
from controllers.utils import validate_email, update_password, validate_password
from streamlit_option_menu import option_menu


class ProfilePage:
    @classmethod
    def update_password_store_user_credentials(self):
        if 'current_password' not in st.session_state:
            st.session_state.email = st.session_state.current_password
        
        if 'password' not in st.session_state:
            st.session_state.password = st.session_state.update_password
        if 'confirm_password' not in st.session_state:
            st.session_state.confirm_password = st.session_state.confirm_update_password
    
    @classmethod
    def profile_page(self):

        clm1, clm2, clm3 = st.columns([1, 3, 1])

        with clm2:
            clm1, clm2, clm3 = st.columns([3, 1, 3])
            with clm2:
                st.title('Perfil')

            selected = option_menu(None, ['Perfil', 'Alterar Senha'],
                                   icons=['person', 'key'],
                                menu_icon="cast", default_index=0, orientation="horizontal",
                                styles={
                "container": {"padding": "0!important", "background-color": "#ffff"},
                "icon": {"color": "#282634", "font-size": "14px"},
                "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#bd928b"},
                "nav-link-selected": {"background-color": "#ff4e44"},
            }
            )

        if selected == 'Perfil':
            self.profile()

        if selected == 'Alterar Senha':
            self.password()

    @classmethod
    def password(self):

        with st.form(key='change_email', clear_on_submit=True):
            email = st.text_input('E-mail:', placeholder='Email', key='email_user')
            new_password = st.text_input(
                'Senha', placeholder='Insira nova senha', type='password', key='update_password')

            confirm_new_password = st.text_input(
                'Senha', placeholder='Confirme a nova senha', type='password', key='confirm_update_password')

            update_password_button = st.form_submit_button(
                label="Salvar", type='primary', on_click=self.update_password_store_user_credentials)

            if update_password_button:
                if new_password != confirm_new_password and (not validate_email(email)):
                    st.warning('Credenciais inválidas')
                    return
                update_password(email, new_password)
                st.success('Senha de funcionário atualizado')

    @classmethod
    def profile(self):

        st.subheader('Nome: ')
        container_name = st.container(border=True)
        container_name.write(f'{st.session_state.user_name}')

        st.subheader('CPF:')
        container_id = st.container(border=True)
        cpf = f'{st.session_state.user_cpf[:3]}.{st.session_state.user_cpf[3:6]}.{
            st.session_state.user_cpf[6:9]}-{st.session_state.user_cpf[9:]}'
        container_id.write(cpf)

        st.subheader('E-mail:')
        container_email = st.container(border=True)
        container_email.write(f'{st.session_state.user_email}')

        st.subheader('Nível de acesso:')
        container_function = st.container(border=True)
        container_function.write(f'{st.session_state.user_access_level}')
        