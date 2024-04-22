import streamlit as st

def log_document_next():
    st.session_state.current_document_page += 1
def log_document_previous():
    if st.session_state.current_document_page > 1:
        st.session_state.current_document_page -= 1 

def log_system_next():
    st.session_state.current_system_page += 1
def log_system_previous():
    if st.session_state.current_system_page > 1:
        st.session_state.current_system_page -= 1

def log_user_next():
    st.session_state.current_user_page += 1
def log_user_previous():
    if st.session_state.current_user_page > 1:
        st.session_state.current_user_page -= 1
