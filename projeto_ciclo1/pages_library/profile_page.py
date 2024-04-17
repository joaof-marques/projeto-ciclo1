import streamlit as st
from pages_library.utils import get_user_profile




def profile_page():
    st.write('')
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