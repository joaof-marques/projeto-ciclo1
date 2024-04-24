import streamlit as st
import re
from controllers.user_controllers import create_user
from database.database import User, engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')

def get_user_emails():

    with Session(bind=engine) as session:
        email = session.query(User.email).all()
        emails = []
        for item in email:
            emails.append(item)
    return emails


def get_usernames():

    with Session(bind=engine) as session:
        name = session.query(User.name).all()
        usernames = []
        for item in name:
            usernames.append(item)
    return usernames


def validate_email(email):

    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):

    pattern = r"^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def validate_cpf(cpf):
    if len(cpf) != 11:
        return False

    cpf_digits_sum = sum(int(cpf[i]) * (10 - i) for i in range(9))
    mod = 11 - (cpf_digits_sum % 11)
    first_digit = mod if mod < 10 else 0


    if int(cpf[9]) != first_digit:
        return False
    
    cpf_digits_sum = sum(int(cpf[i]) * (11 - i) for i in range(10))
    mod = 11 - (cpf_digits_sum % 11)
    second_digit = mod if mod < 10 else 0


    if int(cpf[10]) != second_digit:
        return False
    
    return True

def store_user_credentials():
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

def sign_up():
   
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':red[Cadastro]')
        username = st.text_input('Usuario', key='create_user_username', placeholder='Usuario')
        email = st.text_input('Email', key='create_user_email', placeholder='Email')
        cpf = st.text_input('CPF', key='create_user_cpf', placeholder='CPF')
        password = st.text_input('Senha', key='create_user_password', placeholder='Senha', type='password')
        access_level = st.number_input('Nivel de Acesso', key='create_user_access_level', min_value=1, max_value=4, step=1)
        
        if st.form_submit_button('Enviar'):
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
        
        
# streamlit run projeto_ciclo1\pages_library\signup_page.py