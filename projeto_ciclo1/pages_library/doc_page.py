import streamlit as st
import pandas as pd
import random
from controllers.documents_controllers import create_document, get_document_from_database
from pages_library.utils import show_document_search_results

def doc_page():
    st.write('')
    st.subheader('Documentos')

    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Encontrar', 'Anexar', 'Histórico','Editar', 'Deletar'])


    with tab1:
        st.subheader("Localizar arquivo")

        ## Nome do arquivo
        file_name = st.text_input('Nome do arquivo:')

        ## Filtro de data
        col1, col2 = st.columns(2)
        with col1:
            starting_date = st.date_input("Escolha a data inicial", value=None)

        with col2:
            limit_date = st.date_input("Escolha a data final", value=None)

        ## Filtro funcionário
        register_user = st.text_input("Nome do funcionário que registrou o documento")

        ## Filtro personalizado
        tag = st.multiselect('TAGs', ['Contratos', 'Registros', 'Documentos'])

        ## Botão localizar
        search_button = st.button('Procurar', type='primary')
        
        if search_button:
            files = get_document_from_database(file_name, register_user)
            show_document_search_results(files)
            
        
        st.divider()


    with tab2:
        st.title('Anexar arquivo')

        ## Botão para anexar
        st.file_uploader("Escolha um arquivo:", type=['pdf', 'jpg', 'png', 'jpeg'])

        ## Seletor do tipo de arquivo
        st.radio('Tipo do arquivo:', ['Contrato', 'Registro', 'Documento'])

        ## Selecionar TAG
        tags = st.multiselect('Marcadores', ['Contratos', 'Registros', 'Documentos'])

        st.date_input("Escolha a data do documento:", value=None)

        ## Botão de enviar
        st.button('Enviar')
        

