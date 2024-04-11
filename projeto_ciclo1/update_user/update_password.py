from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from tables import User
import bcrypt

engine = create_engine('postgresql+psycopg2://postgres:12345@localhost/desafio')


def update_password(email, new_password):
    with Session(bind=engine) as session:
        try:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')
            user = session.query(User).filter_by(email = email).first()
            user.password = hashed_password
            session.commit()
            return True, user

        except Exception as error:
            session.rollback()
            print(error)
            return False, None
        
if __name__ == '__main__':
    update_password('eva@example.com', '4321')