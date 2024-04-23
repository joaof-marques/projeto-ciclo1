import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
from projeto_ciclo1.database.database import *
import projeto_ciclo1.pages_library.sparrow_models as spr

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
                        # Convertendo o PDF para uma lista de imagens
                    pages = convert_from_bytes(uploaded_file.read(),
                                            poppler_path=r'poppler-24.02.0\Library\bin')

                    pil_image = pages[0].convert('RGB')
                else:
                    pil_image = Image.open(uploaded_file)
                
                spr.run(pil_image, title)  
                
                st.markdown('---')

        except Exception as e:
            print(e)

    @classmethod
    def model_edit(self):
        try:
            with Session(bind=engine) as session:
                confs = session.query(OcrConfig).all()
                
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
                                session.delete(conf)
                                session.commit()
                                st.rerun()
                    st.markdown('---')
                else:
                    st.title("Sem modelos para gerenciar!")
        except Exception as e:
            session.rollback()
            print(e)
