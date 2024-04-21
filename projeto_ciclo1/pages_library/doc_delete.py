import streamlit as st
from projeto_ciclo1.database.database import *

def delete():
    
    try:
        with Session(bind=engine) as session:
            docs = session.query(Document).all()
            if len(docs) > 0:
                for i, doc in enumerate(docs):

                    lbls = []
                    for row in doc.tags:
                        lbls.append(row)

                    clm1, clm2, clm3, clm4 = st.columns(4)

                    with clm1:
                        st.write(i+1)

                    with clm2:
                        st.write(doc.name)

                    with clm3:
                        st.write(lbls)

                    with clm4:
                        if st.button('Deletar', type='primary', key=f'del_con_{i}'):
                            session.delete(doc)
                            session.commit()
                            st.rerun()
            else:
                st.title("Sem modelos para gerenciar!")
    except Exception as e:
        session.rollback()
        print(e)
