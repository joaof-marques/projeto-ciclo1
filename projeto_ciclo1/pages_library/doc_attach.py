import io
from PIL import Image
import streamlit as st
from ocr.ocr import *
from pdf2image import convert_from_bytes
from database.database import *
from controllers.logs_controllers import Log
import pages_library.sparrow_attach as spr


class Attach:
    
    @classmethod
    def attach(self): 
        
        st.title('Anexar')
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
                
    # Convertion of pdf to img
    @classmethod
    def pdf_convertion(self, pdf):
        pages = convert_from_bytes(pdf.read(), poppler_path=r'poppler-24.02.0\Library\bin')
        image = pages[0].convert('RGB')
        return image
    
                
    @classmethod
    def get_ocr_config(self):     
        with Session(bind=engine) as session:
            all_configs = session.query(OcrConfig)
        return all_configs
    
    
    @classmethod
    def image_2_bytes(self, img):
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        return img_bytes
    
    
    @classmethod
    def rois_convertion(self, rois):
        rois_converted = []

        for row in rois:
            converted = []
            for item in row:
                if item.startswith('(') and item.endswith(')'):
                    num = item.strip('()').split(',')
                    converted.append((int(num[0]), int(num[1])))
                else:
                    converted.append(item)
            rois_converted.append(converted)
            
        return rois_converted
    
    
    @classmethod
    def document_insertion(self, title, img_bytes, tags, text, id_register):
        with Session(bind=engine) as session:
            try:
                doc = Document(name=title, img=img_bytes, tags=tags,
                               content=text, id_register_user=id_register)
                session.add(doc)
                session.commit()
                Log.insert_document_log(st.session_state.user_id, doc.id, 'New document created')
            except Exception as e:
                session.rollback()
                return None


    @classmethod
    def reset_session_rois(self, file):
        if 'actual_file' not in st.session_state:
            st.session_state.actual_file = file.name

        elif st.session_state.actual_file != file.name:
            if 'rois' in st.session_state:
                del st.session_state.rois
            st.session_state.actual_file = file.name


    @classmethod
    def send_form(self, rois, data, img, tags, title, form_key):
        with st.form(key=form_key):
            
            final_text = ''
            
            for i, row in enumerate(rois):
                text = st.text_area(
                    f'{row[2]}', data[i][row[2]], key=f'{form_key}{i}')
                st.markdown("---")
                # Text content for the document insertion
                final_text += f'{row[2]}\n{text}\n'

            if st.form_submit_button('Enviar', type='primary'):
                if title != '':
                    if len(tags) > 0:
                        # Image to bytes
                        img_bytes = self.image_2_bytes(img)
                        # Database insertion
                        self.document_insertion(title, img_bytes, tags, final_text, st.session_state.user_id)
                        st.success('Arquivo Salvo!')
                    else:
                        st.warning('TAGs Vazia!')
                else:
                    st.warning('Título Vazio!')


    @classmethod
    def normal_attach(self):
        
        all_configs = self.get_ocr_config()
        
        models_name = []
        for conf in all_configs:
            models_name.append(conf.name)
                    
        title = st.text_input("Título", key='title_a')
        tags = st.multiselect('Selecionar TAGs', 
                            ['Nota Fiscal', 'Contrato', 'RG', 'CPF', 'Passaporte'],
                            key='insert_tags_a')
        
        option = st.selectbox("Selecionar Modelo",
                            tuple(models_name), key='select_model_1')
        
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
        
                pil_image = self.pdf_convertion(uploaded_file)
            else:
                pil_image = Image.open(uploaded_file)
            
            conf = all_configs.filter_by(name = option).first()
            
            # Images 2 array
            img_bytes = io.BytesIO(conf.img)
            img1 = Image.open(img_bytes)
            array_img1 = np.array(img1)
            array_img2 = np.array(pil_image)

            # Convertion of strings (rois in the database) to values that can be used
            rois_db = conf.rois
            rois = self.rois_convertion(rois_db)
            
            # OCR - read and orientation
            img_new = perspective(array_img1, array_img2)
            data, img_labels = labels(img_new, rois, filter)
            
            img_new = Image.fromarray(img_new)
            
            clm1, clm2 = st.columns(2)
            with clm1:
                st.image(img_labels)
            
            with clm2:
                self.send_form(rois, data, img_new, tags, title, 'send_form_a')
                 
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
            
            self.reset_session_rois(uploaded_file)
                
            if uploaded_file.name.endswith('pdf'):
                pil_image = self.pdf_convertion(uploaded_file)
            else:
                pil_image = Image.open(uploaded_file)
            
            spr.run(pil_image)
            
            st.markdown("---")

            # Call labeling after rois being defined in the sparrow
            if 'rois' in st.session_state and st.session_state.rois is not None:
                
                array_img = np.array(pil_image)
                data, img_labels = labels(array_img, st.session_state.rois, filter)

                clm1, clm2 = st.columns(2)
                
                with clm1:
                    st.image(img_labels)

                with clm2:
                    self.send_form(st.session_state.rois, data, pil_image, tags, title, 'send_form_b')

                st.markdown("---")
        
        elif 'rois' in st.session_state:
            del st.session_state.rois

                
            