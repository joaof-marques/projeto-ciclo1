import streamlit as st


def profile_page():
    st.write('')
    col1, col2, col3 = st.columns(spec=[0.2, 0.1, 0.7])
    
    with col1:

        #st.image('foto_homem.jpg')
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