import streamlit as st
import pandas as pd
from controllers.utils import get_log_user, get_log_documents, get_log_system
from controllers.log_funcions import log_document_next, log_document_previous, log_system_next, log_system_previous, log_user_next, log_user_previous

def store_current_page():
    if 'current_document_page' not in st.session_state:
        st.session_state.current_document_page = 1
    if 'current_system_page' not in st.session_state:
        st.session_state.current_system_page = 1
    if 'current_user_page' not in st.session_state:
        st.session_state.current_user_page = 1

def log_history():
    tab_log_documents, tab_log_system, tab_log_users = st.tabs(['Logs de Documentos', 'Logs do Sistema', 'Logs de Usuários'])
    store_current_page()

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
            previous = st.button('Anterior', key='document_log_previous', on_click=log_document_previous)

        with col2:
            st.write(f'Página {st.session_state.current_document_page}')

        with col3:
            next = st.button('Proximo', key='document_log_next', on_click=log_document_next)

    with tab_log_system:
        _, log_system = get_log_system()

        if log_system is None  or len(log_system) == 0:
            st.title('Nenhum Log Disponível')

        else:
            system_dataframe = pd.DataFrame(log_system)
            st.write(system_dataframe)
        st.markdown("""---""")
        _, col1, col2, col3, _ = st.columns(spec=[.3, .5, .6, .5, .3])

        with col1:
            previous = st.button('Anterior', key='system_log_previous', on_click=log_system_previous)

        with col2:
            st.write(f'Página {st.session_state.current_system_page}')

        with col3:
            next = st.button('Proximo', key='system_log_next', on_click=log_system_next)

    with tab_log_users:
        _, log_user = get_log_user()


        if log_user is None  or len(log_user) == 0:
            st.title('Nenhum Log Disponível')

        else:
            user_dataframe = pd.DataFrame(log_user)
            st.write(user_dataframe)

        st.markdown("""---""")
        _, col1, col2, col3, _ = st.columns(spec=[.3, .5, .6, .5, .3])

        with col1:
            previous = st.button('Anterior', key='user_log_previous', on_click=log_user_previous)

        with col2:
            st.write(f'Página {st.session_state.current_user_page}')

        with col3:
            next = st.button('Proximo', key='user_log_next', on_click=log_user_next)

    