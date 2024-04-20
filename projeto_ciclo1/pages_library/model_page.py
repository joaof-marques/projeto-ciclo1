import streamlit as st
from projeto_ciclo1.database.database import *
import projeto_ciclo1.pages_library.sparrow_models as spr


def models():
    st.title("Modelos")

    tab1, tab2 = st.tabs(['Criar Modelos', 'Gerenciar Modelos'])
    with tab1:
        model_config()

    with tab2:
        model_edit()


def model_config():
    try:
        title = st.text_input("Nome do modelo", key='model_name')
        uploaded_file = st.file_uploader("Selecione um arquivo", type=['png', 'jpg', 'jpeg', 'pdf', 'jfif'])

        if uploaded_file is not None:
            spr.run(uploaded_file, title)  
            
    except Exception as e:
        print(e)


def model_edit():
    try:
        with Session(bind=engine) as session:
            confs = session.query(OcrConfig).all()
            
            if len(confs) > 0:
                for i, conf in enumerate(confs):
                    
                    lbls = []
                    for row in conf.rois:
                        lbls.append(row[2])
                        
                    clm1, clm2, clm3, clm4 = st.columns(4)
                    
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
            
            else:
                st.title("Sem modelos para gerenciar!")
    except Exception as e:
        session.rollback()
        print(e)
