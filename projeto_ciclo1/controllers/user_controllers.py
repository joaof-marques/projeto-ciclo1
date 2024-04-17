from database.database import User, engine, LogUser
from sqlalchemy.orm import Session
from controllers.system_log_controllers import insert_system_log
import bcrypt

def create_user(name, username, email, cpf, password, access_level, logged_user_id):
    
    with Session(bind=engine) as session:        
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(name = name, username = username, email = email, cpf = cpf, password=str(hashed_password.decode('utf-8')), access_level = access_level, deleted=False)
            
            session.add(new_user)
            session.commit()
            
            new_log = LogUser(id_user_modifier=logged_user_id, id_user_modified=new_user.id, log_txt="New User created.")
            
            session.add(new_log)
            session.commit()
            return True, new_user
        except Exception as error:
            session.rollback()
            log_insert_status, log_insert_message = insert_system_log(error)            
            return False, None
        
        
