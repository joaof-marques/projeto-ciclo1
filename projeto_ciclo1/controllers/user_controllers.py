from database.database import User, engine
from sqlalchemy.orm import Session
import bcrypt

def createUser(name, email, cpf, password, access_level):
    
    with Session(bind=engine) as session:
        
        try:
            novo_usuario = User(name = name, email = email, cpf = cpf, password=password, access_level = access_level)
            
            session.add(novo_usuario)
            session.commit()
            return True, f"Usuário {name} cadastrado com Sucesso!"
        except Exception as error:
            session.rollback()
            return False, f"Usuário {name} não pôde ser cadastrado.\n Erro {error}"