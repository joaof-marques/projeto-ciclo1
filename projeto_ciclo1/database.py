from sqlalchemy import create_engine, VARCHAR, INTEGER, TEXT, TIMESTAMP, ARRAY, ForeignKey, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session, relationship
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

# Database info for connection
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
db = os.getenv('DB')

# Conection
url = f'postgresql://{user}:{password}@{host}/{db}'
engine = create_engine(url, echo=True)

# base class for sqlachemy ORM
Base = declarative_base()

# Tables/Classes of the database
# User table
class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    cpf: Mapped[str] = mapped_column(VARCHAR(11), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(20))
    acess_level: Mapped[int] = mapped_column(INTEGER)

    documents = relationship('Document', back_populates='users', cascade='all, delete')
    log_documents = relationship('LogDocument', back_populates='users', cascade='all, delete')
    log_users = relationship('LogUser', back_populates='users', cascade='all, delete')
    
    def __repr__(self):
        return f'{self.id} | {self.name} | {self.email} | {self.cpf} | {self.acess_level}'

# Doc table
class Document(Base):
    __tablename__ = 'documents'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(VARCHAR(255))
    id_register_user: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    register_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    img: Mapped[str] = mapped_column(VARCHAR(255))
    tags: Mapped[list] = mapped_column(ARRAY(VARCHAR))
    content: Mapped[str] = mapped_column(TEXT)
    last_modify: Mapped[str] = mapped_column(TIMESTAMP, default=None)
    id_last_modify_user: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'), default=None)
    
    users = relationship('User', back_populates='documents')
    log_documents = relationship('LogDocument', back_populates='documents')
    
    def __repr__(self):
        return f'{self.id} | {self.type} | {self.id_register_user} | {self.register_date} | {self.img} | {self.tags} | {self.content}| {self.last_modify}| {self.id_last_modify_user}'
    
# Logs tables
class LogUser(Base):
    __tablename__ = 'log_users'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    id_user_modifier: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    id_user_modified: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    log_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    log_txt: Mapped[str] = mapped_column(TEXT)
    
    users = relationship('User', back_populates='log_users')

    def __repr__(self):
        return f'{self.id} | {self.id_user_modifier} | {self.id_user_modified} | {self.log_date} | {self.log_txt}'
    

class LogDocument(Base):
    __tablename__ = 'log_documents'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    id_user_modifier: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    id_document_modified: Mapped[int] = mapped_column(INTEGER, ForeignKey('documents.id'))
    log_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    log_txt: Mapped[str] = mapped_column(TEXT)

    users = relationship('User', back_populates='log_documents')
    documents = relationship('Documents', back_populates='log_documents')

    def __repr__(self):
        return f'{self.id} | {self.id_user_modifier} | {self.id_document_modified} | {self.log_date} | {self.log_txt}'
    

class LogSystem(Base):
    __tablename__ = 'log_system'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    error_type: Mapped[str] = mapped_column(VARCHAR(255))
    log_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    log_txt: Mapped[str] = mapped_column(TEXT)

    def __repr__(self):
        return f'{self.id} | {self.error_type} | {self.log_date} | {self.log_txt}'




if __name__ == '__main__':
    Base.metadata.create_all(engine)
