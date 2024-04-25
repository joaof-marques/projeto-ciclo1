import streamlit as st
import pandas as pd
import os
from controllers.documents_controllers import DocumentControllers as dc
from controllers.utils import show_document_search_results
import math
from io import BytesIO


class SearchPage:
    def draw(): 
        
        st.title("Localizar arquivo")
        file_name = st.text_input('Nome do arquivo:')
        col1, col2 = st.columns(2)
        with col1:
            starting_date = st.date_input("Escolha a data inicial", value=None)

        with col2:
            limit_date = st.date_input("Escolha a data final", value=None)

        register_user = st.text_input("Nome do funcionário que registrou o documento")
        search_button = st.button('Procurar', type='primary')
        
        if 'document_search_current_page' not in st.session_state:
            st.session_state.document_search_current_page = 1
        if 'document_search_pages_quantity' not in st.session_state:
            st.session_state.document_search_pages_quantity = 0          
        if 'selected_file' not in st.session_state:
            st.session_state.selected_file = None
        if 'filtered_files' not in st.session_state:
            st.session_state.filtered_files = None
        
        _, minus_one, display, plus_one, _ = st.columns([0.30, 0.06, 0.04, 0.06, 0.3])

        with minus_one:
            minus = st.button("◀")
            if minus and (st.session_state.document_search_current_page-1) > 0:
                st.session_state.document_search_current_page-=1
        with plus_one:
            plus = st.button("▶") 
            if plus and (st.session_state.document_search_current_page+1) <= st.session_state.document_search_pages_quantity:
                st.session_state.document_search_current_page+=1
        with display:
            st.write(st.session_state.document_search_current_page)
            
        if search_button or minus or plus:
            if st.session_state.document_search_pages_quantity == 0:
                query_result_length = dc.get_query_lenght(file_name, register_user, starting_date, limit_date)
                st.session_state.document_search_pages_quantity = math.ceil(query_result_length/10)
            
            st.session_state.filtered_files = dc.get_document_from_database(file_name, register_user, starting_date, limit_date, st.session_state.document_search_current_page)
        
        if st.session_state.filtered_files:
            show_document_search_results(st.session_state.filtered_files)
        st.divider()
        
        view_document_area = st.container()
        if st.session_state.selected_file:
            details_col, _, img_col = st.columns([0.5,0.1,0.4])

            
            with details_col:
                st.subheader('Nome do documento: ')
                container_name = st.container(border=True)
                container_name.write(st.session_state.selected_file['name'])
                
                st.subheader('Cadastrado por: ')
                container_name = st.container(border=True)
                container_name.write(st.session_state.selected_file['user_register'])

                st.subheader('Tags: ')
                container_name = st.container(border=True)
                with container_name:
                    tag_str = ", ".join(st.session_state.selected_file['tags'])
                    st.markdown(tag_str)
                    
                for key in st.session_state.selected_file['content']:
                    st.subheader(key)
                    container_name = st.container(border=True)
                    container_name.write(st.session_state.selected_file['content'][key])
                    
                st.subheader('Histórico do documento: ') 
                dataframe_data = dc.get_document_log_history(st.session_state.selected_file['id'])
                df = pd.DataFrame(data = dataframe_data)
                st.dataframe(df, column_config={"_index": "Nº", "username": "Nome de Usuário", "log_txt": "Mensagem da modificação", "log_date": "Data da modificação"}, use_container_width=True, )
                

            with img_col:
                _, button2, button1, _ = st.columns([0.4, 0.5, 0.5,0.3])

                with button1:                    
                    delete_button = st.button("Deletar \nDocumento")
                    if delete_button:
                        delete_result = dc.soft_delete_document(st.session_state.selected_file['id'])
                        
                        if delete_result:
                            st.success("Documento deletado com sucesso!")
                        else:
                            st.error("O documento não pôde ser deletado.")
                
                img = BytesIO(st.session_state.selected_file['img'])
                with button2:
                    download_button = st.download_button("Salvar o \ndocumento", img)
                        
                st.image(img)