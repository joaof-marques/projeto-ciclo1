from database.database import User, engine
from sqlalchemy.orm import Session
from controllers.system_log_controllers import insert_system_log
import bcrypt

def create_user(name, email, cpf, password, access_level):
    
    with Session(bind=engine) as session:        
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print(hash)
            novo_usuario = User(name = name, email = email, cpf = cpf, password=str(hashed_password.decode('utf-8')), access_level = access_level)
            
            session.add(novo_usuario)
            session.commit()
            return True, novo_usuario
        except Exception as error:
            session.rollback()
            log_insert_status, log_insert_message = insert_system_log(error)            
            return False, None
        
        
