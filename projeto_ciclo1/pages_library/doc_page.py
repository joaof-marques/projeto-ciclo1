import streamlit as st
import pandas as pd
import random
from streamlit_option_menu import option_menu
from pages_library.doc_models import Models
from pages_library.doc_attach import Attach
from pages_library.search_doc import SearchPage

class DocPage:

    @classmethod
    def doc_page(self):
        clm1, clm2, clm3, clm4, clm5 = st.columns(5)
        with clm3:
            st.title('Documentos')

        selected = option_menu(None, ['Encontrar', 'Anexar', 'Modelos'],
                               icons=['search', 'cloud-upload',
                                      'file-earmark-ruled'],
                               menu_icon="cast", default_index=0, orientation="horizontal",
                               styles={
            "container": {"padding": "0!important", "background-color": "#ffff"},
            "icon": {"color": "#282634", "font-size": "14px"},
            "nav-link": {"color": "#000000", "font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#bd928b"},
            "nav-link-selected": {"background-color": "#ff4e44"},
        }
        )

        if selected == 'Encontrar':
            SearchPage.draw()

        if selected == 'Anexar':
            Attach.attach()

        if selected == 'Modelos':
            Models.models()
