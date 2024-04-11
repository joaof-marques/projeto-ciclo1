import streamlit as st
import random
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, authentication_status, username = authenticator.login()


def doc_page():
    with tab_documentos:
        st.write('')
        st.subheader('Documentos')

        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Encontrar', 'Anexar', 'Histórico','Editar', 'Deletar'])

        with tab1:
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


        with tab2:
            st.title('Anexar arquivo')

            ## Botão para anexar
            st.file_uploader("Escolha um arquivo:")

            ## Seletor do tipo de arquivo
            st.radio('Tipo do arquivo:', ['Contrato', 'Registro', 'Documento'])

            ## Selecionar TAG
            st.multiselect('TAG', ['Contratos', 'Registros', 'Documentos'])

            # Seletor da data do arquivo
            st.date_input("Escolha a data do documento:", value=None)

            ## Botão de enviar
            st.button('Enviar')


def profile_page():
    with tab_perfil:
        st.write('')
        col1, col2, col3 = st.columns(spec=[0.2, 0.1, 0.7])
        
        with col1:
            st.image('foto_homem.jpg')
            st.write('"Nome da pessoa"')

        with col3: 
            st.title('Suas informações:')

            st.subheader('Nome:')
            container_name = st.container(border=True)
            container_name.write('Nome completo')

            st.subheader('CPF:')
            container_id = st.container(border=True)
            container_id.write('000.000.000-00')

            st.subheader('E-mail:')
            container_email = st.container(border=True)
            container_email.write('emailexemplo@exemplo.com')

            st.subheader('Cargo:')
            container_function = st.container(border=True)
            container_function.write('Nome do cargo (nivel de acesso)')


def register_page():
    with tab_cadastro:
        st.write('')
        st.subheader('Cadastro de funcionário:')

        tab1, tab2, tab3 = st.tabs(['Cadastrar', 'Alterar', 'Deletar'])

        with tab1:
            with st.form(key='register'):
                name = st.text_input('Nome:')
                pin = st.text_input('CPF:')
                email = st.text_input('E-mail:')
                role = st.text_input('Função:')
                submit_button = st.form_submit_button(label="Registrar")

                if submit_button:
                    st.write('Funcionário cadastrado')

        with tab2:
            team = st.selectbox(
                "Funcionários: ",
                ('Fulano', 'Ciclano', 'Beltrano', 'Tiago', 'Joãos', 'Feliphe'),
                index=None,
                placeholder="Selecione o funcionário"
                )
            
            st.divider()

            with st.form(key='Alterar'):
                name = st.text_input('Nome:')
                pin = st.text_input('CPF:')
                email = st.text_input('E-mail:')
                role = st.text_input('Função:')
                submit_button = st.form_submit_button(label="Salvar")
                if submit_button:
                    st.write('Funcionário cadastrado')

        with tab3:
            team = st.selectbox(
                'Funcionários: ', 
                ('Fulano', 'Ciclano', 'Beltrano', 'Tiago', 'Joãos', 'Feliphe'),
                placeholder="Selecione o funcionário"
                )

            del_funcionário = st.button('Excluir', type='primary')

            if del_funcionário:
                st.write('Funcionário excluido com sucesso!')


def main_page():    
    if st.session_state["authentication_status"]:
        ## HOME      
        with tab_home:
            st.subheader('Navegue pelas páginas')
            st.divider() 

        ## Documentos
        doc_page()


        ## -- Perfil --
        profile_page()


        ## -- Cadastro --
        register_page()


    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')

    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

## Body
tab_home, tab_documentos, tab_perfil, tab_cadastro = st.tabs(['Home', 'Documentos', 'Perfil', 'Cadastro'])
main_page()
authenticator.logout()
