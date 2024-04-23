import streamlit as st
import pandas as pd
import os
from controllers.documents_controllers import get_document_from_database, get_query_lenght, soft_delete_document, get_document_log_history
from pages_library.utils import show_document_search_results
import math


class SearhPage:
    def draw():
        
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
        # tag = st.multiselect('TAGs', ['Contratos', 'Registros', 'Documentos'])

        ## Botão localizar
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
                query_result_length = get_query_lenght(file_name, register_user, starting_date, limit_date)
                st.session_state.document_search_pages_quantity = math.ceil(query_result_length/10)
            
            st.session_state.filtered_files = get_document_from_database(file_name, register_user, starting_date, limit_date, st.session_state.document_search_current_page)
        
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
                
                st.subheader('Tipo de documento: ')
                container_name = st.container(border=True)
                container_name.write(st.session_state.selected_file['type'])
                
                st.subheader('Cadastrado por: ')
                container_name = st.container(border=True)
                container_name.write(st.session_state.selected_file['user_register'])

                st.subheader('Tags: ')
                container_name = st.container(border=True)
                with container_name:
                    tag_str = ", ".join(st.session_state.selected_file['tags'])
                    st.markdown(tag_str)
                    
                st.subheader('Histórico do documento: ') 
                dataframe_data = get_document_log_history(st.session_state.selected_file['id'])
                df = pd.DataFrame(data = dataframe_data)
                st.dataframe(df, column_config={"_index": "Nº", "username": "Nome de Usuário", "log_txt": "Mensagem da modificação", "log_date": "Data da modificação"}, use_container_width=True, )
                

            with img_col:
                _, button, _ = st.columns([0.4,0.5,0.3])

                with button:                    
                    delete_button = st.button("Deletar Documento")
                    if delete_button:
                        delete_result = soft_delete_document(st.session_state.selected_file['id'])
                        
                        if delete_result:
                            st.success("Documento deletado com sucesso!")
                        else:
                            st.error("O documento não pôde ser deletado.")
                        
                dir_path = os.path.dirname(__file__)
                root_path = os.path.dirname(dir_path)
                doc_image_path = os.path.join(root_path, st.session_state.selected_file['img'])
                st.image(doc_image_path)

    

