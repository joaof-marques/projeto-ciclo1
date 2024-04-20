import streamlit as st
from pdf2image import convert_from_bytes


uploaded_file = st.file_uploader('Inserir arquivo', type=[
                                 'png', 'jpg', 'jpeg', 'pdf', 'jfif'])

if uploaded_file is not None and uploaded_file.name.endswith('pdf') :
    # Convertendo o PDF para uma lista de imagens
    pages = convert_from_bytes(uploaded_file.read(), poppler_path=r'projeto_ciclo1\poppler-24.02.0\Library\bin')
    
    # Exibindo as imagens
    for i, page in enumerate(pages):
        st.image(page, caption=f"Página {i+1}", use_column_width=True)


# streamlit run projeto_ciclo1\pages_library\test_pdf.py