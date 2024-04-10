import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    st.title(f'Bem vindo *{st.session_state["name"]}*')  
    st.divider()
    st.subheader('Navegue pelas páginas:')
    st.write('')
    st.page_link('pages/1Perfil.py', label= 'Perfil')
    st.page_link('pages/2Documentos.py', label= 'Documentos')
    st.page_link('pages/3Cadastro.py', label= 'Cadastro')
    st.divider() 
    authenticator.logout()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# if st.session_state["authentication_status"]:
#     try:
#         if authenticator.reset_password(st.session_state["username"]):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)


