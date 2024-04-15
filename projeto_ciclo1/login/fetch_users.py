from database.database import User
from sqlalchemy.orm import Session
from database.database import engine

def fetch_users():
    with Session(bind=engine) as session:
        users = session.query(User).all()

    return True, users
