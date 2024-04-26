from database.database import LogSystem, LogUser, LogDocument, engine
from sqlalchemy.orm import Session
import streamlit as st
import time

class Log:
    
    @classmethod  
    def insert_system_log(self, error):
        with Session(bind=engine) as session:
            try:
                error_log_system = LogSystem(error_type=type(error).__name__, log_txt=error.__str__())
                session.add(error_log_system)
                session.commit()
                return True, "Log de erro de sistema registrado com sucesso."
            except Exception as e:
                session.rollback()            
                return False, f"Não foi possível registrar o log de erro. Contate o administrador do sistema.\n Erro {e}"
            

    @classmethod
    def insert_user_log(self, modifier, modified, text):
        with Session(bind=engine) as session:
            try:
                user_log_system = LogUser(id_user_modifier=modifier,  
                                        id_user_modified=modified, 
                                        log_txt=text)
                session.add(user_log_system)
                session.commit()
                return True, "Log do usuário registrado com sucesso."
            except Exception as e:
                session.rollback()
                return False, f"Não foi possível registrar o log do usuário. Contate o administrador do sistema.\n Erro {e}"


    @classmethod
    def insert_document_log(self, modifier, modified, text):
        with Session(bind=engine) as session:
            try:
                doc_log_system = LogDocument(id_user_modifier=modifier,  
                                        id_document_modified=modified,
                                        log_txt=text)
                session.add(doc_log_system)
                session.commit()
                return True, "Log do documento registrado com sucesso."
            except Exception as e:
                session.rollback()
                return False, f"Não foi possível registrar o log do documento. Contate o administrador do sistema.\n Erro {e}"
