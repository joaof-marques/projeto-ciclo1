import streamlit as st
import re
from controllers.user_controllers import create_user
from controllers.system_log_controllers import insert_system_log
from database.database import engine, User, LogUser, LogDocument, LogSystem
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv
import os
import bcrypt

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
            return True, user

        except Exception as error:
            insert_system_log(error)
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
            return True, user

        except Exception as error:
            insert_system_log(error)
            session.rollback()
            return False, None
        
def delete_user(email, cpf):
    with Session(bind=engine) as session:
        try:
            user = session.query(User).filter_by(email = email).filter_by(cpf = cpf).first()
            user.deleted = True
            session.commit()
            return True, user
        
        except Exception as error:
            insert_system_log(error)
            session.rollback()
            return False, None
        
def get_user_profile(username):
    try:
        with Session(bind=engine) as session:
            user = session.query(User).filter_by(username = username).first()
            user_credentials = {'id': user.id, 'name': user.name, 'cpf': user.cpf, 'email': user.email, 'access_level': user.access_level}
 
            return True, user_credentials
    except Exception as error:

            insert_system_log(error)
            session.rollback()
            return False, None

def get_log_user():
    try:
        with Session(bind=engine) as session:
            logs = session.query(LogUser).all()
            log_user = [
                {
                    'log_id': log.id,
                    'modifier_id': log.id_user_modifier,
                    'modifier_name': log.user_modifier.name,
                    'modified_id': log.id_user_modified,
                    'modified_name': log.user_modified.name,
                    'log_date': f'{log.log_date.day}/{log.log_date.month}/{log.log_date.year} - {log.log_date.hour}:{log.log_date.minute}:{log.log_date.microsecond}',
                    'log_txt': log.log_txt,
                }
                for log in logs
            ]

            return True, log_user

    except Exception as error:

            insert_system_log(error)
            session.rollback()
            return False, None
    
def get_log_documents():
    try:
        with Session(bind=engine) as session:
            logs = session.query(LogDocument).all()
            log_documents = [
                {
                    'log_id': log.id,
                    'modifier': f'{log.id_user_modifier} - {log.user.name}',
                    'document_modified_id': f'{log.id_document_modified} - {log.document.name}',
                    'log_date': f'{log.log_date.day}/{log.log_date.month}/{log.log_date.year} - {log.log_date.hour}:{log.log_date.minute}:{log.log_date.microsecond}',
                    'log_txt': log.log_txt,
                }
                for log in logs
            ]

        return True, log_documents

    except Exception as error:

            insert_system_log(error)
            session.rollback()
            return False, None
    
def get_log_system():
    try:
        with Session(bind=engine) as session:
            logs = session.query(LogSystem).all()
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

            insert_system_log(error)
            session.rollback()
            return False, None