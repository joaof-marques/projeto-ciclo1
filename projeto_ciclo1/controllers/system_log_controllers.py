from database.database import LogSystem, engine
from sqlalchemy.orm import Session
import time

def insert_system_log(error):
    
    with Session(bind=engine) as session:
        try:
            error_log_system = LogSystem(error_type = type(error), log_date = time.time(), log_txt = error)
            session.add(error_log_system)
            session.commit()
            return True, "Log de erro de sistema registrado com sucesso."
        except Exception as e:
            session.rollback()            
            return False, f"Não foi possível registrar log de erro. Contate o administrador do sistema.\n Erro {e}"