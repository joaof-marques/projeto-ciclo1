import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
from database.database import *
from pages_library.sparrow import Sparrow
from controllers.utils import get_models
from math import ceil

class Models:
    @classmethod
    def models(self):
        st.title("Modelos")

        tab1, tab2 = st.tabs(['Criar Modelos', 'Gerenciar Modelos'])
        with tab1:
            Models.model_config()

        with tab2:
            Models.model_edit()

    @classmethod
    def model_config(self):
        try:
            title = st.text_input("Nome do modelo", key='model_name')
            uploaded_file = st.file_uploader("Selecione um arquivo", type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'])
            

            st.markdown('---')

            if uploaded_file is not None:
                if uploaded_file.name.endswith('pdf'):
                    pages = convert_from_bytes(uploaded_file.read(), poppler_path=os.path.join(os.path.dirname(__file__), r'poppler-24.02.0\Library\bin'))
                    pil_image = pages[0].convert('RGB')
                else:
                    pil_image = Image.open(uploaded_file)
                
                Sparrow.run_save(pil_image, title)  
                
                st.markdown('---')

        except Exception as e:
            print(e)

    @classmethod
    def model_edit(self):
            self.store_index_count()
            self.store_current_page()
            self.manage_models_max_page()
            
            _, confs = get_models()
                
            if len(confs) > 0:
                for i, conf in enumerate(confs):
                    
                    lbls = []
                    for row in conf.rois:
                        lbls.append(row[2])
                        
                    clm1, clm2, clm3, clm4 = st.columns([1, 1, 3, 1])
                    
                    with clm1:
                        st.write(i+1)
                    
                    with clm2:
                        st.write(conf.name)
                        
                    with clm3:
                        st.write(tuple([lbl for lbl in lbls]))
                        
                    with clm4:
                        if st.button('Deletar', type='primary', key=f'del_con_{i}'):
                            try:
                                with Session(bind=engine) as session:
                                    session.delete(conf)
                                    session.commit()
                                    st.rerun()
                            except Exception as e:
                                session.rollback()
                                print(e)
        

            st.markdown('---')
            _, col1, col2, col3, _ = st.columns(spec=[.3, .06, .04, .06, .3])

            with col1:
                previous = st.button('Anterior', key='models_previous', on_click=self.manage_models_previous)

            with col2:
                st.write(f'Página {st.session_state.current_manage_models_page}')

            with col3:
                next = st.button('Proximo', key='models_next', on_click=self.manage_models_next)

        
    
    @classmethod
    def store_current_page(self):
        if 'current_manage_models_page' not in st.session_state:
            st.session_state.current_manage_models_page = 1
    @classmethod
    def store_index_count(self):
        if 'index_model_page' not in st.session_state:
            st.session_state.index_models_page = 0
    
    @classmethod
    def manage_models_max_page(self):
        with Session(bind=engine) as session:
            models = session.query(OcrConfig).count()
            st.session_state.manage_model_max_page = ceil(models / 10)
    
    @classmethod
    def manage_models_next(self):
        if st.session_state.current_manage_models_page < st.session_state.manage_model_max_page:
            st.session_state.current_manage_models_page += 1
            st.session_state.index_models_page += 1

    @classmethod
    def manage_models_previous(self):
        if st.session_state.current_manage_models_page > 1:
            st.session_state.current_manage_models_page -= 1 
            st.session_state.index_models_page -= 1
