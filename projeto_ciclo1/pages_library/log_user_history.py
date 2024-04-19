import streamlit as st
import pandas as pd
from controllers.utils import get_log_user, get_log_documents, get_log_system
def log_history():
    tab_log_documents, tab_log_system, tab_log_users = st.tabs(['Logs de Documentos', 'Logs do Sistema', 'Logs de Usuários'])

    with tab_log_documents:
        _, log_document = get_log_documents()

        if log_document is None or len(log_document) == 0:
            st.title('Nenhum Log Disponível')

        else:
            document_dataframe = pd.DataFrame(log_document)
            st.write(document_dataframe)

    with tab_log_system:
        _, log_system = get_log_system()

        if log_system is None  or len(log_system) == 0:
            st.title('Nenhum Log Disponível')

        else:
            system_dataframe = pd.DataFrame(log_system)
            st.write(system_dataframe)


    with tab_log_users:
        _, log_user = get_log_user()


        if log_user is None  or len(log_user) == 0:
            st.title('Nenhum Log Disponível')

        else:
            user_dataframe = pd.DataFrame(log_user)
            st.write(user_dataframe)

    