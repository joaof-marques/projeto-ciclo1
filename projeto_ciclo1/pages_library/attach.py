import streamlit as st
from projeto_ciclo1.ocr.ocr import *
from PIL import Image
from projeto_ciclo1.database.database import *
from streamlit_extras.stylable_container import stylable_container
import io

def attach():
    st.title("Anexar Arquivo")
    
    with Session(bind=engine) as session:
        all_configs = session.query(OcrConfig)
        lbl = []
        for conf in all_configs:
            lbl.append(conf.name)
        
    option = st.selectbox("Selecione uma modelo",
                         tuple(lbl))
    
    filter = st.selectbox("Selecione um filtro", ('Padrão', 'Filtro1'))
    
    uploaded_file = st.file_uploader("Selecione um arquivo", type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'], key='uploader_file')


    if uploaded_file is not None and option:

        with Session(bind=engine) as session:
            conf = all_configs.filter(OcrConfig.name == option).first()
            img_bytes = io.BytesIO(conf.img)
            img1 = Image.open(img_bytes)
            array_img1 = np.array(img1)
            roi_db = conf.rois
            roi = []
    
            for row in roi_db:
                converted = []
                for item in row:
                    if item.startswith('(') and item.endswith(')'):
                        # Remover os parênteses e dividir os números
                        num = item.strip('()').split(',')
                        # Converter os núm para inteiros e adicioná-los à lista
                        converted.append((int(num[0]), int(num[1])))
                    else:
                        # Se não for uma tupla, apenas adicioná-lo à lista sem conversão
                        converted.append(item)
                roi.append(converted)
            
        img2 = Image.open(uploaded_file)
        array_img2 = np.array(img2)
        
        img_new = perspective(array_img1, array_img2)
        
        data, img_labels = labels(img_new, roi, filter)
        
        # Exibir o título se fornecido pelo usuário
        clm1, clm2 = st.columns(2)
        with clm1:
            st.image(img_labels)
        
        with clm2:
            for i, row in enumerate(roi):
                text = st.text_input(f"{row[2]}", data[i][row[2]], key=i)
        
        # Show image
        
        

        
        with stylable_container("red", css_styles="""
                        button {
                            background-color: #3C41F5;
                        }""",
        ): 
            if st.button('Enviar', key='send_button'):
                # st.balloons()
                pass
            

