import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER, DB_PASSWORD, DB_HOST, DB_NAME = os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_NAME')


URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


def authenticate(email, password):
   
    engine = create_engine(URL)  
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return True, user
    else:
        return False, None

def login_auth():
    st.write('Cadastro')
        
    email = st.text_input('Email')
    password = st.text_input('Senha', type='password')

    if st.button('Enviar'):
        _, user = authenticate(email, password)
        print(user)
        if user:
            st.success(f'Logged in as {user.name}')
            return True, user
        else:
            st.error('Invalid email or password')
            return False, None


def main():
    login_auth()

if __name__ == '__main__':
    main()
