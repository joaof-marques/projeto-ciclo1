import streamlit as st
import pandas as pd
from controllers.utils import get_log_user, get_log_documents, get_log_system
from math import ceil
from database.database import engine, LogDocument, LogSystem, LogUser
from sqlalchemy.orm import Session

class LogHistory:
    @classmethod
    def store_current_page(self):
        if 'current_document_page' not in st.session_state:
            st.session_state.current_document_page = 1
        if 'current_system_page' not in st.session_state:
            st.session_state.current_system_page = 1
        if 'current_user_page' not in st.session_state:
            st.session_state.current_user_page = 1

    @classmethod
    def log_history(self):
        tab_log_documents, tab_log_system, tab_log_users = st.tabs(['Logs de Documentos', 'Logs do Sistema', 'Logs de Usuários'])
        self.store_current_page()
        self.log_document_max_page()
        self.log_system_max_page()
        self.log_user_max_page()

        with tab_log_documents:
            _, log_document = get_log_documents()

            if log_document is None or len(log_document) == 0:
                st.title('Nenhum Log Disponível')

            else:
                document_dataframe = pd.DataFrame(log_document)
                st.write(document_dataframe)
            
            st.markdown("""---""")
            _, col1, col2, col3, _ = st.columns(spec=[.3, .06, .04, .06, .3])

            with col1:
                previous = st.button('Anterior', key='document_log_previous', on_click=self.log_document_previous)

            with col2:
                st.write(f'Página {st.session_state.current_document_page}')

            with col3:
                next = st.button('Proximo', key='document_log_next', on_click=self.log_document_next)

        with tab_log_system:
            _, log_system = get_log_system()

            if log_system is None  or len(log_system) == 0:
                st.title('Nenhum Log Disponível')

            else:
                system_dataframe = pd.DataFrame(log_system)
                st.write(system_dataframe)
            st.markdown("""---""")
            _, col1, col2, col3, _ = st.columns(spec=[.3, .06, .04, .06, .3])

            with col1:
                previous = st.button('Anterior', key='system_log_previous', on_click=self.log_system_previous)

            with col2:
                st.write(f'Página {st.session_state.current_system_page}')

            with col3:
                next = st.button('Proximo', key='system_log_next', on_click=self.log_system_next)

        with tab_log_users:
            _, log_user = get_log_user()


            if log_user is None  or len(log_user) == 0:
                st.title('Nenhum Log Disponível')

            else:
                user_dataframe = pd.DataFrame(log_user)
                st.write(user_dataframe)

            st.markdown("""---""")
            _, col1, col2, col3, _ = st.columns(spec=[.3, .06, .04, .06, .3])

            with col1:
                previous = st.button('Anterior', key='user_log_previous', on_click=self.log_user_previous)

            with col2:
                st.write(f'Página {st.session_state.current_user_page}')

            with col3:
                next = st.button('Proximo', key='user_log_next', on_click=self.log_user_next)

    @classmethod
    def log_document_max_page(self):
        with Session(bind=engine) as session:
            document_max_page = session.query(LogDocument).count()
            st.session_state.log_document_max_page = ceil(document_max_page / 10)

    @classmethod
    def log_document_next(self):
        if st.session_state.current_document_page < st.session_state.log_document_max_page:
            st.session_state.current_document_page += 1

    @classmethod
    def log_document_previous(self):
        if st.session_state.current_document_page > 1:
            st.session_state.current_document_page -= 1 

    @classmethod
    def log_system_max_page(self):
        with Session(bind=engine) as session:
            system_max_page = session.query(LogSystem).count()
            st.session_state.log_system_max_page = ceil(system_max_page / 10)

    @classmethod
    def log_system_next(self):
        if st.session_state.current_system_page < st.session_state.log_system_max_page:
            st.session_state.current_system_page += 1

    @classmethod
    def log_system_previous(self):
        if st.session_state.current_system_page > 1:
            st.session_state.current_system_page -= 1

    @classmethod
    def log_user_max_page(self):
        with Session(bind=engine) as session:
            user_max_page = session.query(LogUser).count()
            st.session_state.log_user_max_page = ceil(user_max_page / 10)

    @classmethod
    def log_user_next(self):
        if st.session_state.current_user_page < st.session_state.log_user_max_page:
            st.session_state.current_user_page += 1

    @classmethod
    def log_user_previous(self):
        if st.session_state.current_user_page > 1:
            st.session_state.current_user_page -= 1


        