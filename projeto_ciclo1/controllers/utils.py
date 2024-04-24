import re
import streamlit as st
from controllers.logs_controllers import Log
from database.database import engine, User, LogUser, LogDocument, LogSystem, Document
from sqlalchemy.orm import Session
import bcrypt


def get_user_emails():

    with Session(bind=engine) as session:
        email = session.query(User.email).all()
        emails = []
        for item in email:
            emails.append(item)
    return emails


def get_usernames():

    with Session(bind=engine) as session:
        name = session.query(User.username).all()
        usernames = []
        for item in name:
            usernames.append(item)
    return usernames

def fetch_users():
    with Session(bind=engine) as session:
        users = session.query(User).all()
        user_credentials = [{'email': user.email, 'username': user.username, 'password': user.password} for user in users]
    return True, user_credentials


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

def validate_name(name):

    pattern = r"^[a-zA-ZÀ-ú\s]*$"
    if re.match(pattern, name):
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

def update_email(lost_email, new_email):
    with Session(bind=engine) as session:
        try: 
            user = session.query(User).filter_by(email = lost_email).first()
            user.email = new_email
            session.commit()
            return True, None

        except Exception as error:
            Log.insert_system_log(error)
            session.rollback()
            return False, None
        
def validate_password(email, current_password):
    with Session(bind=engine) as session:
        try:
            user = session.query(User).filter_by(email = email).first()
            print(type(current_password))
            if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):

                return True
            return False

        except Exception as error:
            Log.insert_system_log(error)
            session.rollback()
            return False, None

def update_password(email, new_password):
    with Session(bind=engine) as session:
        try:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')
            user = session.query(User).filter_by(email = email).first()
            user.password = hashed_password
            session.commit()
            return True, None

        except Exception as error:
            Log.insert_system_log(error)
            session.rollback()
            return False, None
        
def delete_user(email, cpf):
    with Session(bind=engine) as session:
        try:
            user = session.query(User).filter_by(email = email).filter_by(cpf = cpf).first()
            user.deleted = True
            session.commit()
            return True, None
        
        except Exception as error:
            Log.insert_system_log(error)
            session.rollback()
            return False, None
        
def get_user_profile(username):
    try:
        with Session(bind=engine) as session:
            user = session.query(User).filter_by(username = username).first()
            user_credentials = {'id': user.id, 'name': user.name, 'cpf': user.cpf, 'email': user.email, 'access_level': user.access_level}
 
            return True, user_credentials
    except Exception as error:

            Log.insert_system_log(error)
            session.rollback()
            return False, None
    
def get_log_documents():
    try:
        with Session(bind=engine) as session:
            logs = session.query(LogDocument).slice(10 * (st.session_state.current_document_page - 1), (10 * (st.session_state.current_document_page - 1))+ 10).all()
            log_documents = [
                {
                    'log_id': log.id,
                    'modifier': f'{log.user.name}',
                    'document_modified_id': f'{log.document.name}',
                    'log_date': f'{log.log_date.day}/{log.log_date.month}/{log.log_date.year} - {log.log_date.hour}:{log.log_date.minute}:{log.log_date.microsecond}',
                    'log_txt': log.log_txt,
                }
                for log in logs
            ]

        return True, log_documents

    except Exception as error:

            Log.insert_system_log(error)
            session.rollback()
            return False, None
    
def get_log_system():
    try:
        with Session(bind=engine) as session:
            logs = session.query(LogSystem).slice(10 * (st.session_state.current_system_page - 1), (10 * (st.session_state.current_system_page - 1))+ 10).all()
            log_system = [
                {
                    'log_id': log.id,
                    'error_type': log.error_type,
                    'log_date': f'{log.log_date.day}/{log.log_date.month}/{log.log_date.year} - {log.log_date.hour}:{log.log_date.minute}:{log.log_date.microsecond}',
                    'log_txt': log.log_txt,
                }
                for log in logs
            ]

        return True, log_system

    except Exception as error:

            Log.insert_system_log(error)
            session.rollback()
            return False, None

def get_log_user():
    try:
        with Session(bind=engine) as session:
            logs = session.query(LogUser).slice(10 * (st.session_state.current_user_page - 1), (10 * (st.session_state.current_user_page - 1))+ 10).all()
            log_user = [
                {
                    'log_id': log.id,
                    'modifier_name': log.user_modifier.name,
                    'modified_name': log.user_modified.name,
                    'log_date': f'{log.log_date.day}/{log.log_date.month}/{log.log_date.year} - {log.log_date.hour}:{log.log_date.minute}:{log.log_date.microsecond}',
                    'log_txt': log.log_txt,
                }
                for log in logs
            ]
            return True, log_user

    except Exception as error:

            Log.insert_system_log(error)
            session.rollback()
            return False, None
        
def show_document_search_results(files):
    
    id_column, name_column, date_column, detail_column = st.columns([0.1, 0.5, 0.2, 0.2])
    with id_column:
        st.subheader('Id')
    with name_column:
        st.subheader('Nome do documento')
    with date_column:
        st.subheader('Data')
    with detail_column:
        st.subheader('Detalhes')
        
    for file in files:     
        id_column, name_column, date_column, detail_column = st.columns([0.1, 0.5, 0.2, 0.2])  
        with id_column:
            st.write(file['id'])
        with name_column:
            st.write(file['name'])
        with date_column:
            st.write(file['register_date'].strftime("%d/%m/%Y"))
        with detail_column:
            st.button("Detalhes", on_click=set_file_to_details_area, args=[file,] , key=file)
    

def set_file_to_details_area(file):
    st.session_state.selected_file = file
    