import streamlit as st
from controllers.utils import validate_email, update_password

class ProfilePage:
    @classmethod
    def update_password_store_user_credentials(self):
            if 'email' not in st.session_state:
                st.session_state.email = st.session_state.email_user
            
            if 'password' not in st.session_state:
                st.session_state.password = st.session_state.update_password
    
    @classmethod
    def profile_page(self):
        tab_user_profile, tab_update_password = st.tabs(['Perfil', 'Alterar Senha'])

        with tab_user_profile:
            col1, col2, col3 = st.columns(spec=[0.2, 0.1, 0.7])
        
            with col1:

                #st.image('foto_homem.jpg')
                st.write(f'{st.session_state.user_name}')

            with col3: 
                st.title('Suas informações:')

                st.subheader('Nome: ')
                container_name = st.container(border=True)
                container_name.write(f'{st.session_state.user_name}')

                st.subheader('CPF:')
                container_id = st.container(border=True)
                cpf = f'{st.session_state.user_cpf[:3]}.{st.session_state.user_cpf[3:6]}.{st.session_state.user_cpf[6:9]}-{st.session_state.user_cpf[9:]}'
                container_id.write(cpf)

                st.subheader('E-mail:')
                container_email = st.container(border=True)
                container_email.write(f'{st.session_state.user_email}')

                st.subheader('Cargo:')
                container_function = st.container(border=True)
                container_function.write(f'Nível de acesso {st.session_state.user_access_level}')

        with tab_update_password:
            with st.form(key='change_email', clear_on_submit=True):
                email = st.text_input('E-mail:', placeholder='Email', key='email_user')
                new_password = st.text_input('Senha', placeholder='Insira nova senha', type='password', key='update_password')

                confirm_new_password = st.text_input('Senha', placeholder='Confirme a nova senha', type='password', key='confirm_update_password')
                
                update_password_button = st.form_submit_button(label="Salvar", type='primary', on_click=self.update_password_store_user_credentials)
                if update_password_button:
                    if new_password != confirm_new_password and (not validate_email(email)):
                        st.warning('Credenciais inválidas')
                        return 
                    update_password(email, new_password)
                    st.success('Senha de funcionário atualizado')
