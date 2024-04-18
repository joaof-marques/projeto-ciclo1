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
        normal_attach()
    
    with tab2:
        fast_attach()
    
            

def normal_attach():
    with Session(bind=engine) as session:
            all_configs = session.query(OcrConfig)
            lbl = []
            for conf in all_configs:
                lbl.append(conf.name)
    title = st.text_input("Título", key='title_a')
    option = st.selectbox("Selecionar Modelo", tuple(lbl), key='select_model_1')
    
    filter = st.selectbox("Selecionar Filtro", ('Padrão', 'Tratamento de Ruido'), key='select_filter_1')
    
    uploaded_file = st.file_uploader("Selecionar Arquivo", type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'], key='uploader_file_1')


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
            for i, row in enumerate(rois):
                text = st.text_input(f"{row[2]}", data[i][row[2]], key=i)
        
        
        # Enviar conteudo para o banco de dados
        with stylable_container("red", css_styles="""
                        button {
                            background-color: #3C41F5;
                        }""",
        ): 
            if st.button('Enviar', key='send_button'):
                st.balloons()
                
            
            
def fast_attach():
    title = st.text_input("Título", key='title_b')

    filter = st.selectbox("Selecionar Filtro", ('Padrão', 'Tratamento de Ruido'), key='select_filter_2')

    uploaded_file = st.file_uploader("Selecionar Arquivo", type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'], key='uploader_file_2')

    if uploaded_file is not None:

        rois = spr.run(uploaded_file)

        if rois is not None:
            # Convertendo imagem em array
            img = Image.open(uploaded_file)
            array_img = np.array(img)

            data, img_labels = labels(array_img, rois, filter)

            # Exibir imagem e colunas
            clm1, clm2 = st.columns(2)
            with clm1:
                img_labels = cv.resize(img_labels, (int(900 * 75 / 100), int(1280 * 75 / 100)))
                st.image(img_labels)

            with clm2:
                with st.form(key="send_form"):
                    for i, row in enumerate(rois):
                        text = st.text_input(
                            f"{row[2]}", data[i][row[2]], key=i)
                    
                     # Enviar conteudo para o banco de dados
                    with stylable_container("red", css_styles="""
                                button {
                                    background-color: #3C41F5;
                                }""",
                                            ):
                        
                        if st.form_submit_button('Enviar', type='primary'):
                            st.balloons()

