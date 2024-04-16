import streamlit as st
import streamlit_authenticator as stauth
from projeto_ciclo1.controllers.system_log_controllers import insert_system_log
from projeto_ciclo1.login.fetch_users import fetch_users
from projeto_ciclo1.pages_library.main import main

try:
    _, users = fetch_users()
    emails = []
    usernames = []
    passwords = []
    for user in users:
        emails.append(user.email)
        usernames.append(user.name)
        passwords.append(user.password)

    credentials = {'usernames': {}}

    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='StreamLit', cookie_key='abcdef', cookie_expiry_days=0)

    email, authentication_status, username = Authenticator.login()

    if username:
        if username in usernames:
            if authentication_status:
                st.sidebar.subheader(f'Welcome {username}')
                # Implementar paginas
                main()

                Authenticator.logout()
            else:
                st.warning('Usuario não existe')

except Exception as error:
    st.warning('Erro no sistema')
    insert_system_log(error)

