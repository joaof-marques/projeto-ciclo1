import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from controllers.utils import get_log_user, get_log_documents, get_log_system
from math import ceil
from database.database import engine, LogDocument, LogSystem, LogUser
from sqlalchemy.orm import Session

class LogHistory:
    @classmethod
    def store_index_count(self):
        if 'index_user_count' not in st.session_state:
            st.session_state.index_user_count = 0
        if 'index_system_count' not in st.session_state:
            st.session_state.index_system_count = 0
        if 'index_document_count' not in st.session_state:
            st.session_state.index_document_count = 0

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
        clm1, clm2, clm3 = st.columns(spec=[8, 1, 8])
        with clm2:
            st.title('Logs')
            
        selected = option_menu(None, ['Logs de Documentos', 'Logs do Sistema', 'Logs de Usuários'],
                               icons=['file-earmark-text', 'file-earmark-code','file-earmark-person'],
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
        self.store_index_count()

        if selected == 'Logs de Documentos':
            self.log_documents_tab()

        if selected == 'Logs do Sistema':
            self.log_system_tab()
        
        if selected == 'Logs de Usuários':
            self.log_users_tab()
    
    @classmethod
    def log_documents_tab(self):
        _, log_document = get_log_documents()

        st.markdown("""---""")
        if log_document is None or len(log_document) == 0:
            c1, c2, c3 = st.columns(spec=[3, 4, 2])
            with c2:
                st.title('Nenhum Log Disponível')
            
        else:
            _, c2, c3, c4, c5 = st.columns(5)

            with c2:
                st.subheader('Modificante')
            with c3:
                st.subheader('Modificado')
            with c4:
                st.subheader('Date')
            with c5:
                st.subheader('Texto')

            for index, log in enumerate(log_document):
                c1, c2, c3, c4, c5= st.columns(5)
                with c1:
                    st.write((st.session_state.index_document_count * 10) + (index + 1))     
                with c2:
                    st.write(log['document_modifier_id'])
                with c3:
                    st.write(log['document_modified_id'])
                with c4:
                    st.write(log['log_date'])
                with c5:
                    st.write(log['log_txt'])
    
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

        st.markdown("""---""")
        if log_system is None  or len(log_system) == 0:
            c1, c2, c3 = st.columns(spec=[3, 4, 2])
            with c2:
                st.title('Nenhum Log Disponível')


        else:
            _, c2, c3, c4 = st.columns(4)

            with c2:
                st.subheader('Erro')
            with c3:
                st.subheader('Data')
            with c4:
                st.subheader('texto')


            for index, log in enumerate(log_system):
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.write((st.session_state.index_system_count * 10) + (index + 1))     
                with c2:
                    st.write(log['error_type'])
                with c3:
                    st.write(log['log_date'])
                with c4:
                    st.write(log['log_txt'])

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

        st.markdown("""---""")
        if log_user is None  or len(log_user) == 0:
            c1, c2, c3 = st.columns([3, 4, 2])
            with c2:
                st.title('Nenhum Log Disponível')

        else:
            _, c2, c3, c4, c5 = st.columns(5)

            with c2:
                st.subheader('Modificante')
            with c3:
                st.subheader('Modificado')
            with c4:
                st.subheader('Data')
            with c5:
                st.subheader('Texto')

            for index, log in enumerate(log_user):
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    st.write((st.session_state.index_user_count * 10) + (index + 1))     
                with c2:
                    st.write(log['modifier_name'])
                with c3:
                    st.write(log['modified_name'])
                with c4:
                    st.write(log['log_date'])
                with c5:
                    st.write(log['log_txt'])


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
            st.session_state.index_document_count += 1

    @classmethod
    def log_document_previous(self):
        if st.session_state.current_document_page > 1:
            st.session_state.current_document_page -= 1 
            st.session_state.index_document_count -= 1


    @classmethod
    def log_system_max_page(self):
        with Session(bind=engine) as session:
            system_max_page = session.query(LogSystem).count()
            st.session_state.log_system_max_page = ceil(system_max_page / 10)

    @classmethod
    def log_system_next(self):
        if st.session_state.current_system_page < st.session_state.log_system_max_page:
            st.session_state.current_system_page += 1
            st.session_state.index_system_count += 1

    @classmethod
    def log_system_previous(self):
        if st.session_state.current_system_page > 1:
            st.session_state.current_system_page -= 1
            st.session_state.index_system_count -= 1

    @classmethod
    def log_user_max_page(self):
        with Session(bind=engine) as session:
            user_max_page = session.query(LogUser).count()
            st.session_state.log_user_max_page = ceil(user_max_page / 10)

    @classmethod
    def log_user_next(self):
        if st.session_state.current_user_page < st.session_state.log_user_max_page:
            st.session_state.current_user_page += 1
            st.session_state.index_user_count += 1


    @classmethod
    def log_user_previous(self):
        if st.session_state.current_user_page > 1:
            st.session_state.current_user_page -= 1
            st.session_state.index_user_count -= 1



        