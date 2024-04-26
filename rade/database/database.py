from sqlalchemy import create_engine, VARCHAR, INTEGER, TEXT, TIMESTAMP, ARRAY, ForeignKey, BOOLEAN, func, Table, LargeBinary, Index
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session, relationship
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

# Database info for connection
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')

# Conection
url = f'postgresql://{user}:{password}@{host}/{db}'
engine = create_engine(url, echo=False)

# base class for sqlachemy ORM
Base = declarative_base()

# Tables/Classes of the database
# User table
class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    username:Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    cpf: Mapped[str] = mapped_column(VARCHAR(11), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(255))
    access_level: Mapped[int] = mapped_column(INTEGER)
    deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    
    document_register = relationship('Document', back_populates='user_register', cascade='all, delete')
    log_document = relationship('LogDocument', back_populates='user', cascade='all, delete')
    log_user_modifier = relationship('LogUser', back_populates='user_modifier', foreign_keys='LogUser.id_user_modifier', cascade='all, delete')
    log_user_modified = relationship('LogUser', back_populates='user_modified', foreign_keys='LogUser.id_user_modified', cascade='all, delete')
    
    id_index = Index('id_index_user', id, postgresql_using='hash')
    name_index = Index('name_index_user', name)
    username_index = Index('username_index_user', username, postgresql_using='hash')
    email_index = Index('email_index_user', email, postgresql_using='hash')
    cpf_index = Index('cpf_index_user', cpf, postgresql_using='hash')
    
    def __repr__(self):
        return f'{self.id} | {self.name} | {self.email} | {self.cpf} | {self.access_level}'

# Doc table
class Document(Base):
    __tablename__ = 'documents'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    id_register_user: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    register_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    img: Mapped[str] = mapped_column(LargeBinary)
    tags: Mapped[list] = mapped_column(ARRAY(VARCHAR))
    content: Mapped[str] = mapped_column(TEXT)
    deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False)
   
    user_register = relationship('User', back_populates='document_register')
    log_document = relationship('LogDocument', back_populates='document', cascade='all, delete')
    
    id_index = Index('id_index_doc', id, postgresql_using='hash')
    name_index = Index('name_index_doc', name)
    id_register_index = Index('id_register_index_doc', id_register_user, postgresql_using='hash')
    date_register_index = Index('date_register_index_doc', register_date)
    tags_index = Index('tags_index_doc', tags, postgresql_using='gin')
    
    def __repr__(self):
        return f'{self.id} | {self.id_register_user} | {self.register_date} | {self.tags} | {self.content}'
    
# Logs tables
class LogUser(Base):
    __tablename__ = 'log_users'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    id_user_modifier: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    id_user_modified: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    log_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    log_txt: Mapped[str] = mapped_column(TEXT)
    
    user_modifier = relationship('User', back_populates='log_user_modifier', foreign_keys=[id_user_modifier])
    user_modified = relationship('User', back_populates='log_user_modified', foreign_keys=[id_user_modified])
    
    id_index = Index('id_index_log_user', id, postgresql_using='hash')
    modifier_index = Index('modifier_index_log_user', id_user_modifier, postgresql_using='hash')
    modified_index = Index('modified_index_log_user', id_user_modified, postgresql_using='hash')
    date_index = Index('date_index_log_user', log_date)

    def __repr__(self):
        return f'{self.id} | {self.id_user_modifier} | {self.id_user_modified} | {self.log_date} | {self.log_txt}'
    

class LogDocument(Base):
    __tablename__ = 'log_documents'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    id_user_modifier: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    id_document_modified: Mapped[int] = mapped_column(INTEGER, ForeignKey('documents.id'))
    log_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    log_txt: Mapped[str] = mapped_column(TEXT)

    user = relationship('User', back_populates='log_document')
    document = relationship('Document', back_populates='log_document')

    id_index = Index('id_index_log_doc', id, postgresql_using='hash')
    modifier_index = Index('modifier_index_log_doc', id_user_modifier, postgresql_using='hash')
    modified_index = Index('modified_index_log_doc', id_document_modified, postgresql_using='hash')
    date_index = Index('date_index_log_doc', log_date)
    
    def __repr__(self):
        return f'{self.id} | {self.id_user_modifier} | {self.id_document_modified} | {self.log_date} | {self.log_txt}'
    

class LogSystem(Base):
    __tablename__ = 'log_system'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    error_type: Mapped[str] = mapped_column(VARCHAR(255))
    log_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    log_txt: Mapped[str] = mapped_column(TEXT)

    id_index = Index('id_index_log_sys', id, postgresql_using='hash')
    type_index = Index('type_index_log_sys', error_type)
    date_index = Index('date_index_log_sys', log_date)
    
    def __repr__(self):
        return f'{self.id} | {self.error_type} | {self.log_date} | {self.log_txt}'


class OcrConfig(Base):
    __tablename__ = 'ocr_config'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    img: Mapped[str] = mapped_column(LargeBinary)
    rois: Mapped[list] = mapped_column(ARRAY(VARCHAR))

    id_index = Index('id_index_ocr_config', id, postgresql_using='hash')
    name_index = Index('name_index_ocr_config', name)

    def __repr__(self):
        return f'{self.id} | {self.name} | {self.img} | {self.rois}'
    
# Create tables on postgre
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    # with Session(bind=engine) as session:
    #     session.add(User(name='Feliphe', username='batata', cpf='12345678911', email='bat@ta', password='123', access_level=4))
    #     session.commit()
