from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from projeto_ciclo1.database import User

engine = create_engine('postgresql+psycopg2://postgres:12345@localhost/desafio')


def update_password(lost_email, new_email):
    with Session(bind=engine) as session:
        try: 
            user = session.query(User).filter_by(email = lost_email).first()
            user.email = new_email
            session.commit()
            return True, user

        except Exception as error:
            session.rollback()
            print(error)
            return False, None
        
if __name__ == '__main__':
    update_password('eva@example.com', 'evona@example.com')