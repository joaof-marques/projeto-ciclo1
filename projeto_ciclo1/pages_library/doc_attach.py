import io
from PIL import Image
import streamlit as st
import streamlit_javascript as st_js
from projeto_ciclo1.ocr.ocr import *
from pdf2image import convert_from_bytes
from projeto_ciclo1.database.database import *
import projeto_ciclo1.pages_library.sparrow_attach as spr
from streamlit_extras.stylable_container import stylable_container

class Attach:
    
    @classmethod
    def attach(self):
        st.title("Anexar Arquivo")
        
        tab1, tab2 = st.tabs(['Anexo com modelo', 'Anexo sem modelo'])
        with tab1:
            try:
                self.normal_attach()
            except Exception as e:
                print(e)
                
        with tab2:
            try:
                self.fast_attach()
            except Exception as e:
                print(e)
                
    @classmethod
    def normal_attach(self):
        with Session(bind=engine) as session:
                all_configs = session.query(OcrConfig)
                lbls = []
                for conf in all_configs:
                    lbls.append(conf.name)
                    
        title = st.text_input("Título", key='title_a')
        tags = st.multiselect('Selecionar TAGs', 
                            ['Nota Fiscal', 'Contrato', 'RG', 'CPF', 'Passaporte'],
                            key='insert_tags_a')
        
        option = st.selectbox("Selecionar Modelo",
                            tuple(lbls), key='select_model_1')
        
        filter = st.selectbox("Selecionar Filtro",
                            ('Padrão', 'Tratamento de Ruido'),
                            key='select_filter_1')
        
        uploaded_file = st.file_uploader("Selecionar Arquivo",
                                        type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'],
                                        key='uploader_file_1')

        st.markdown("---")

        if uploaded_file is not None and option:
            
            # Convertion of pdf to img
            if uploaded_file.name.endswith('pdf'):
        
                pages = convert_from_bytes(uploaded_file.read(),
                                        poppler_path=r'poppler-24.02.0\Library\bin')

                pil_image = pages[0].convert('RGB')
                
            else:
                pil_image = Image.open(uploaded_file)
                
            # Get selected OCR-config 
            with Session(bind=engine) as session:
                conf = all_configs.filter_by(name = option).first()
                
                # Imagem byte -> array
                img_bytes = io.BytesIO(conf.img)
                img1 = Image.open(img_bytes)
                array_img1 = np.array(img1)
                
                roi_db = conf.rois
                
            # Convertion of strings (rois in the database) to values that can be used
            rois = []
        
            for row in roi_db:
                converted = []
                for item in row:
                    if item.startswith('(') and item.endswith(')'):
                        num = item.strip('()').split(',')
                        converted.append((int(num[0]), int(num[1])))
                    else:
                        converted.append(item)
                rois.append(converted)
            
            
            array_img2 = np.array(pil_image)
            
            # OCR - read and orientation
            img_new = perspective(array_img1, array_img2)
            data, img_labels = labels(img_new, rois, filter)
            
            
            clm1, clm2 = st.columns(2)
            with clm1:
                st.image(img_labels)
            
            with clm2:
                with st.form(key="send_form_a"):

                    final_text = ''
                    
                    for i, row in enumerate(rois):
                        text = st.text_area(f'{row[2]}', data[i][row[2]], key=f'text_area_a{i}')
                        
                        # Text content for the document insertion
                        final_text += f'{row[2]}\n{text}\n'
                        st.markdown("---")

                    if st.form_submit_button('Enviar', type='primary'): 
                        if len(tags) > 0 and title != '':
                            
                            # Image to bytes
                            buffer = io.BytesIO()
                            img_new = Image.fromarray(img_new)
                            img_new.save(buffer, format='PNG')
                            img_bytes = buffer.getvalue()
                            
                            # Database insertion
                            with Session(bind=engine) as session:
                                try:
                                    session.add(Document(name=title, img=img_bytes, tags=tags, content=final_text, id_register_user=st.session_state.user_id))
                                    session.commit()
                                except Exception as e:
                                    session.rollback()
                        else:
                            raise Exception('Campo Vazio!')
                        
            st.markdown("---")

    @classmethod
    def fast_attach(self):
        title = st.text_input("Título", key='title_b')
        
        tags = st.multiselect('Selecionar TAGs', 
                            ['Nota Fiscal', 'Contrato', 'RG', 'CPF', 'Passaporte'], 
                            key='insert_tags_b')

        filter = st.selectbox("Selecionar Filtro", 
                            ('Padrão', 'Tratamento de Ruido'), 
                            key='select_filter_2')
        
        uploaded_file = st.file_uploader("Selecionar Arquivo", 
                                        type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'], 
                                        key='uploader_file_2')
            
        st.markdown("---")

        if uploaded_file is not None:
            
            # Reset rois if the file change
            if 'actual_file' not in st.session_state:
                st.session_state.actual_file = uploaded_file.name
                
            elif st.session_state.actual_file != uploaded_file.name:
                if 'rois' in st.session_state:
                    del st.session_state.rois
                st.session_state.actual_file = uploaded_file.name
                
            # Convertion of pdf to img
            if uploaded_file.name.endswith('pdf'):
                
                pages = convert_from_bytes(uploaded_file.read(), 
                                        poppler_path=r'poppler-24.02.0\Library\bin')
                
                pil_image = pages[0].convert('RGB')
                
            else:
                pil_image = Image.open(uploaded_file)
            
            # Call sparrow
            spr.run(pil_image)
            
            st.markdown("---")

            # Call labeling after rois being defined in the sparrow
            if 'rois' in st.session_state and st.session_state.rois is not None:
                
                array_img = np.array(pil_image)
                data, img_labels = labels(array_img, st.session_state.rois, filter)

                clm1, clm2 = st.columns(2)
                with clm1:
                    img_labels = cv.resize(img_labels, 
                                        (int(900 * 70 / 100),  
                                            int(1280 * 70 / 100)))
                    st.image(img_labels)

                with clm2:
                    with st.form(key="send_form_b"):
                        
                        final_text = ''
                        
                        for i, row in enumerate(st.session_state.rois):
                            text = st.text_area(
                                f"{row[2]} ", data[i][row[2]], key=f'text_area_b{i}')
                            
                            # Text content for the document insertion
                            final_text += f'{row[2]}\n{text}\n'
                            
                            st.markdown("---")
                        
                        if st.form_submit_button('Enviar', type='primary'):
                            try:
                                if len(tags) > 0 and title != '':
                                    
                                    # Imago to bytes
                                    buffer = io.BytesIO()
                                    pil_image.save(buffer, format='PNG')
                                    img_bytes = buffer.getvalue()

                                    # Database insertion
                                    with Session(bind=engine) as session:
                                        try:
                                            session.add(Document(name=title, img=img_bytes, tags=tags,
                                                        content=final_text, id_register_user=st.session_state.user_id))
                                            session.commit()
                                                    
                                        except Exception as e:
                                            print(e)
                                            session.rollback()
                    
                                    st.rerun()
                                else:
                                    raise Exception('Campo Vazio!')
                            except Exception as e:
                                print(e)
                                
                st.markdown("---")
        
        elif 'rois' in st.session_state:
            del st.session_state.rois

                
            