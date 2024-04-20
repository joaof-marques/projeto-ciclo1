import io
from PIL import Image
import streamlit as st
from projeto_ciclo1.ocr.ocr import *
from projeto_ciclo1.database.database import *
import projeto_ciclo1.pages_library.sparrow_scan as spr
from streamlit_extras.stylable_container import stylable_container

def attach():
    st.title("Anexar Arquivo")
    
    tab1, tab2 = st.tabs(['Anexo com modelo', 'Anexo sem modelo'])
    with tab1:
        try:
            normal_attach()
        except Exception as e:
            print(e)
    with tab2:
        try:
            fast_attach()
            
        except Exception as e:
            print(e)
            

def normal_attach():
    with Session(bind=engine) as session:
            all_configs = session.query(OcrConfig)
            lbls = []
            for conf in all_configs:
                lbls.append(conf.name)
                
    title = st.text_input("Título", key='title_a')
    tags = st.multiselect('Selecionar Tag', 
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


    if uploaded_file is not None and option:

        # Extraindo a configuração definida pelo usuário
        with Session(bind=engine) as session:
            conf = all_configs.filter(OcrConfig.name == option).first()
            
            # Imagem byte -> array
            img_bytes = io.BytesIO(conf.img)
            img1 = Image.open(img_bytes)
            array_img1 = np.array(img1)
            
            # Regiões de interesse
            roi_db = conf.rois
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
        
        
        # Convertendo imagem em array
        img2 = Image.open(uploaded_file)
        array_img2 = np.array(img2)
        
        # implementando funcionalidade do orc - reorientação e leitura
        img_new = perspective(array_img1, array_img2)
        data, img_labels = labels(img_new, rois, filter)
        
        # Exibir imagem e colunas
        clm1, clm2 = st.columns(2)
        with clm1:
            st.image(img_labels)
        
        with clm2:
            with st.form(key="send_form_a"):

                final_text = ''
                for i, row in enumerate(rois):
                    text = st.text_area(f'{row[2]}', data[i][row[2]], key=f'text_area_a{i}')
                    final_text += f'{row[2]}\n{text}\n'
                    st.markdown("---")

                if st.form_submit_button('Enviar', type='primary'): 
                    if len(tags) > 0 and title != '':
                        # Image to bytes
                        docImg = Image.open(uploaded_file)
                        buffer = io.BytesIO()
                        docImg.save(buffer, format='PNG')
                        img_bytes = buffer.getvalue()
                        
                        with Session(bind=engine) as session:
                            try:
                                session.add(Document(name=title, img=img_bytes, tags=tags, content=final_text, id_register_user=st.session_state.user_id))
                                session.commit()
                            except Exception as e:
                                session.rollback()
                    else:
                        raise Exception('Campo Vazio!')
                       
            
def fast_attach():
    title = st.text_input("Título", key='title_b')
    tags = st.multiselect('Selecionar Tag', 
                          ['Nota Fiscal', 'Contrato', 'RG', 'CPF', 'Passaporte'], 
                          key='insert_tags_b')

    filter = st.selectbox("Selecionar Filtro", 
                          ('Padrão', 'Tratamento de Ruido'), 
                          key='select_filter_2')
    uploaded_file = st.file_uploader("Selecionar Arquivo", 
                                    type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'], 
                                    key='uploader_file_2')
    
    def send():
        try:
            if len(tags) > 0 and title != '':
                docImg = Image.open(uploaded_file)
                buffer = io.BytesIO()
                docImg.save(buffer, format='PNG')
                img_bytes = buffer.getvalue()

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
            
    if uploaded_file is not None:
        # if 'rois' not in st.session_state or st.session_state.rois == None:
        #     st.session_state.rois = None
        #     while st.session_state.rois == None:
        #         st.session_state.rois = spr.run(uploaded_file)
    
        rois = spr.run(uploaded_file)
        
        if rois is not None:
            
            img = Image.open(uploaded_file)
            array_img = np.array(img)
            data, img_labels = labels(array_img, rois, filter)

            # Exibir imagem e colunas
            clm1, clm2 = st.columns(2)
            with clm1:
                img_labels = cv.resize(img_labels, 
                                       (int(900 * 75 / 100), int(1280 * 75 / 100)))
                st.image(img_labels)

            with clm2:
                with st.form(key="send_form_b"):
                    final_text = ''
                    
                    for i, row in enumerate(rois):
                        text = st.text_area(
                            f"{row[2]}", data[i][row[2]], key=f'text_area_b{i}')
                        final_text += f'{row[2]}\n{text}\n'
                        st.markdown("---")
                    
                    st.form_submit_button('Enviar', type='primary', on_click=send)
                
            