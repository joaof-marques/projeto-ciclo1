from database.database import User, engine, LogUser
from sqlalchemy.orm import Session
from controllers.logs_controllers import Log
import bcrypt


class UserControllers:
    @classmethod
    def create_user(self, name, username, email, cpf, password, access_level, logged_user_id):
        
        with Session(bind=engine) as session:        
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                new_user = User(name = name, username = username, email = email, cpf = cpf, password=str(hashed_password.decode('utf-8')), access_level = access_level, deleted=False)
                
                session.add(new_user)
                session.commit()
                
                Log.insert_user_log(logged_user_id, new_user.id, "New User created.")

                return True, new_user
            except Exception as error:
                session.rollback()
                log_insert_status, log_insert_message = Log.insert_system_log(error)            
                return False, None
        
        
