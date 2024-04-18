from sqlalchemy.orm import Session
from projeto_ciclo1.database.database import User
from projeto_ciclo1.database.database import engine

def fetch_users():
    with Session(bind=engine) as session:
        users = session.query(User).all()

    return True, users
