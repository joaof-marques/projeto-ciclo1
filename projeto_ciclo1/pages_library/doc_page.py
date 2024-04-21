import streamlit as st
import pandas as pd
import random
from streamlit_option_menu import option_menu
from projeto_ciclo1.pages_library.doc_models import models
from projeto_ciclo1.pages_library.doc_attach import attach

def doc_page():
    clm1, clm2, clm3, clm4, clm5 = st.columns(5)
    with clm3:
        st.title('Documentos')

    selected = option_menu(None, ['Encontrar', 'Anexar','Modelos'],
                            icons=['search', 'cloud-upload','file-earmark-ruled'],
                            menu_icon="cast", default_index=0, orientation="horizontal", 
                            styles={
                                "container": {"padding": "0!important", "background-color": "#ffff"},
                                "icon": {"color": "#282634", "font-size": "14px"},
                                "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#bd928b"},
                                "nav-link-selected": {"background-color": "#ff4e44"},
                            }
    )

    if selected == 'Encontrar':
        st.subheader("Localizar arquivo")

        ## Nome do arquivo
        st.text_input('Nome do arquivo:')

        ## Filtro de data
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Escolha a data inicial", value=None)

        with col2:
            st.date_input("Escolha a data final", value=None)

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

    if selected == 'Anexar':
        attach()

    if selected == 'Modelos':
        models()
        