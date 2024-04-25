from database.database import Document, User, LogDocument, engine
from sqlalchemy.orm import Session
import datetime, json


class DocumentControllers:

    @classmethod
    def get_query_lenght(self, file_name, user_register_name, starting_date=None, limit_date=None):
        
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

    @classmethod
    def get_document_from_database(self, file_name, user_register_name, starting_date=None, limit_date=None, page=1):
        
        if starting_date is None:
            starting_date = datetime.datetime(1900, 1, 1)
        if limit_date is None:
            limit_date = datetime.datetime(2100, 12, 31)
        
        starting_date += datetime.timedelta(days=1)
        limit_date += datetime.timedelta(days=1)
        
        with Session(bind=engine) as session:
            
            try:
                
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
                    'id_register_user': document.id_register_user,
                    'img': document.img,
                    'tags':document.tags,
                    'content': json.loads(document.content),
                    'doc_history':document.log_document,
                    'user_register': document.user_register.name,
                    'register_date': document.register_date
                    } for document in query_result]
                
                return commom_objects_result
            except Exception as e:
                session.rollback()
                print(e)
                return False
     
    @classmethod       
    def soft_delete_document(self, document_id):
        with Session(bind=engine) as session:
            try:    
                
                document = session.query(Document)\
                    .filter(Document.id == document_id).all()
                
                document[0].deleted = True   

                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(e)
                return False
        

    @classmethod
    def get_document_log_history(self, document_id):
        
        with Session(bind=engine) as session:
            try:
                query_result = session.query(LogDocument)\
                .filter(LogDocument.id_document_modified==document_id)\
                .all()
                found_logs = [{'username': log.user.username, 'log_txt': log.log_txt, 'log_date': log.log_date} for log in query_result]

                return found_logs
            except Exception as e:
                session.rollback()
                print(e)
                return False