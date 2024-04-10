import streamlit as st

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