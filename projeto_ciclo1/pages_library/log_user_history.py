import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from controllers.utils import get_log_user, get_log_documents, get_log_system
# from controllers.log_funcions import log_document_next, log_document_previous, log_document_max_page, log_system_next, log_system_previous, log_system_max_page, log_user_next, log_user_previous, log_user_max_page
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
        clm1, clm2, clm3 = st.columns([8, 1, 8])
        with clm2:
            st.title('Logs')
            
        selected = option_menu(None, ['Logs de Documentos', 'Logs do Sistema', 'Logs de Usuários'],
                            icons=['search', 'cloud-upload',
                                    'file-earmark-ruled'],
                            menu_icon="cast", default_index=0, orientation="horizontal",
                            styles={
            "container": {"padding": "0!important", "background-color": "#ffff"},
            "icon": {"color": "#282634", "font-size": "14px"},
            "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#bd928b"},
            "nav-link-selected": {"background-color": "#ff4e44"},
        }
        )
        
        self.store_current_page()
        self.log_document_max_page()
        self.log_system_max_page()
        self.log_user_max_page()

        if selected == 'Logs de Documentos':
            self.log_documents_tab()

        if selected == 'Logs do Sistema':
            self.log_system_tab()
        
        if selected == 'Logs de Usuários':
            self.log_users_tab()
    
    @classmethod
    def log_documents_tab(self):
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
                
    @classmethod
    def log_system_tab(self):
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

        
    @classmethod
    def log_users_tab(self):
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


        