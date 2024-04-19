from database.database import Document, User, engine
from sqlalchemy.orm import Session
from controllers.system_log_controllers import insert_system_log
from time import time
import datetime
import os

def create_document(new_file, document_type,user_id, content, tags:list=[]):
    relative_path = save_document_get_path(new_file)
    
    #content will come from OCR reading when inserting a document on the front end page, so this will not be necessary
    # change this to the OCR method when ready
    content = new_file.getvalue()

    with Session(bind=engine) as session:
        try:           
            new_document = Document(name=new_file.name, type=document_type, id_register_user=user_id, img=relative_path, tags=tags, content=content, deleted=False)
            
            session.add(new_document)
            session.commit()
            
            return True, new_document
        except Exception as error:
            session.rollback()
            insert_system_log(error)
        
        
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

def get_query_lenght(file_name, user_register_name, starting_date=None, limit_date=None):
    
    if starting_date is None:
        starting_date = datetime.datetime(1900, 1, 1)
    if limit_date is None:
        limit_date = datetime.datetime(2100, 12, 31)

    starting_date += datetime.timedelta(days=1)
    limit_date += datetime.timedelta(days=1)
    
    with Session(bind=engine) as session:
        
        query_results_size = session.query(Document)\
            .join(User, Document.id_register_user == User.id)\
            .filter(
                Document.name.ilike(f'%{file_name}%'),
                User.name.ilike(f'%{user_register_name}%'),
                Document.register_date >= starting_date,
                Document.register_date <= limit_date
                )\
            .where(Document.deleted.is_(False))\
            .count()
            
        return query_results_size

def get_document_from_database(file_name, user_register_name, starting_date=None, limit_date=None, page=1):
    
    if starting_date is None:
        starting_date = datetime.datetime(1900, 1, 1)
    if limit_date is None:
        limit_date = datetime.datetime(2100, 12, 31)
    
    starting_date += datetime.timedelta(days=1)
    limit_date += datetime.timedelta(days=1)
    
    with Session(bind=engine) as session:
        
        query_result = session.query(Document)\
            .join(User, Document.id_register_user == User.id)\
            .filter(
                Document.name.ilike(f'%{file_name}%'),
                User.name.ilike(f'%{user_register_name}%'),
                Document.register_date >= starting_date,
                Document.register_date <= limit_date
                )\
            .where(Document.deleted.is_(False))\
            .order_by(Document.register_date)\
            .slice(10 * (page-1), (10 * (page-1))+10)\
            .all()
        
        commom_objects_result = [{
            'id': document.id, 'name': document.name,
            'type': document.type,
            'id_register_user': document.id_register_user,
            'img': document.img,
            'tags':document.tags,
            'content': document.content,
            'doc_history':document.log_document,
            'user_register': document.user_register.name,
            'register_date': document.register_date
            } for document in query_result]
        
        return commom_objects_result
        
        

if __name__ == '__main__':
    pass