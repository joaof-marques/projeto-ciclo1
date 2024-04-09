from database.database import User, engine
from sqlalchemy.orm import Session
from controllers.system_log_controllers import insert_system_log
import bcrypt, time

def createUser(name, email, cpf, password, access_level):
    
    with Session(bind=engine) as session:        
        try:            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            novo_usuario = User(name = name, email = email, cpf = cpf, password=hashed_password, access_level = access_level)
            
            session.add(novo_usuario)
            session.commit()
            return True, f"Usuário {name} cadastrado com Sucesso!"
        except Exception as error:
            session.rollback()
            log_insert_status, log_insert_message = insert_system_log(error)            
            return False, f"Usuário {name} não pôde ser cadastrado.\n Erro {error}"