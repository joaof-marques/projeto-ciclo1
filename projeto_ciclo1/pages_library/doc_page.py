import streamlit as st
import pandas as pd
import random
from controllers.documents_controllers import create_document

def doc_page():
    st.write('')
    st.subheader('Documentos')

    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Encontrar', 'Anexar', 'Histórico','Editar', 'Deletar'])


    with tab1:
        st.subheader("Localizar arquivo")

        ## Nome do arquivo
        file_name = st.text_input('Nome do arquivo:')

        ## Filtro de data
        col1, col2 = st.columns(2)
        with col1:
            starting_date = st.date_input("Escolha a data inicial", value=None)

        with col2:
            limit_date = st.date_input("Escolha a data final", value=None)

        ## Filtro funcionário
        team = st.selectbox(
        "Funcionário: ",
        ('Fulano', 'Ciclano', 'Beltrano', 'Tiago', 'Joãos', 'Feliphe'),
        index=None,
        placeholder="Selecione o funcionário"
        )

        ## Filtro personalizado
        tag = st.multiselect('TAGs', ['Contratos', 'Registros', 'Documentos'])

        ## Botão localizar
        st.button('Procurar', type='primary')
        
        st.divider()

        ## Exibidor dos arquivos
        df = pd.DataFrame(
            {
                "Nome": ["Documento1", "Documento2", "Documento3"],
                "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
                "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
            }
        )
        st.dataframe(
            df,
            column_config={
                "Nome": "Documento",
                "url": st.column_config.LinkColumn("App URL"),
                "views_history": st.column_config.LineChartColumn(
                    "Visualização (últimos 30 dias)", y_min=0, y_max=5000
                ),
            },
            hide_index=True,
        )


    with tab2:
        st.title('Anexar arquivo')

        ## Botão para anexar
        file = st.file_uploader("Escolha um arquivo:", type=['pdf', 'jpg', 'png', 'jpeg'])

        ## Seletor do tipo de arquivo
        document_type = st.radio('Tipo do arquivo:', ['Contrato', 'Registro', 'Documento'])

        ## Selecionar TAG
        tags = st.multiselect('Marcadores', ['Contratos', 'Registros', 'Documentos', 'Em andamento', 'CNH', 'RG', 'CPF', 'Recibo'])

        ocr_model = st.selectbox('Selecione o modelo de documento', ['OCR_model1', 'OCR_model2', 'OCR_model3'])
        
        # Seletor da data do arquivo
        # st.date_input("Escolha a data do documento:", value=None)

        ## Botão de enviar
        st.button(
            label='Enviar',
            on_click=create_document,
            args=[file, document_type, st.session_state.user_id, ocr_model, tags]
        )

