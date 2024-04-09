import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User # Caminho para a tabela User da classe SQLAlchemy
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DB_USER, DB_PASSWORD, DB_HOST, DB_NAME = os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_NAME')


# URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

def authenticate(email, password):
    engine = create_engine('postgresql+psycopg2://postgres:12345@localhost/desafio')  
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(email=email, password=password).first()
    session.close()
    return user


def login_page():
    st.title('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        user = authenticate(email, password)
        if user:
            st.success(f'Logged in as {user.name}')
            return True
        else:
            st.error('Invalid email or password')
            return False



def main():
    login_page()

if __name__ == '__main__':
    main()
