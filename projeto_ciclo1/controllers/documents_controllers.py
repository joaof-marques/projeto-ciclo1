from database.database import Document, engine
from sqlalchemy.orm import Session
from controllers.system_log_controllers import insert_system_log
from time import time
import os

def create_document(new_file, user_id, tags:list=[]):
    
    relative_path = save_document_get_path(new_file)
    
    # change this to the OCR method when done
    content = new_file.read()    
        
    with Session(bind=engine) as session:
        
        new_document = Document(type=new_file.type, id_register_user=user_id, register_date=time(), img=relative_path, tags=tags, content=content)
        
def save_document_get_path(new_file):
    
    '''This funcion saves the file into the file system and returns the path to the file relative to the root folder.'''
    
    controllers_path = os.path.dirname(__file__)
    src_path = os.path.dirname(controllers_path)
    documents_path = os.path.join(src_path, "documents")
    
    # Create folder "documents" if not exists
    os.makedirs(documents_path, exist_ok=True)
    
    file_path = os.path.join(documents_path, new_file.name)
    
    with open(file_path, "wb") as f:
        f.write(new_file.read())
    
    
    return os.path.relpath(file_path, src_path)

if __name__ == '__main__':
    pass