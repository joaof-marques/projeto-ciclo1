from sqlalchemy import create_engine, VARCHAR, INTEGER, TEXT, TIMESTAMP, ARRAY, ForeignKey, BOOLEAN, func, Table, LargeBinary
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
engine = create_engine(url)

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
    password: Mapped[str] = mapped_column(VARCHAR(255))
    access_level: Mapped[int] = mapped_column(INTEGER)
    deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    
    document_register = relationship('Document', back_populates='user_register', cascade='all, delete')
    log_document = relationship('LogDocument', back_populates='user', cascade='all, delete')
    log_user_modifier = relationship('LogUser', back_populates='user_modifier', foreign_keys='LogUser.id_user_modifier', cascade='all, delete')
    log_user_modified = relationship('LogUser', back_populates='user_modified', foreign_keys='LogUser.id_user_modified', cascade='all, delete')
    
    def __repr__(self):
        return f'{self.id} | {self.name} | {self.email} | {self.cpf} | {self.access_level}'

# Doc table
class Document(Base):
    __tablename__ = 'documents'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    type: Mapped[str] = mapped_column(VARCHAR(255))
    id_register_user: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    register_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    img: Mapped[str] = mapped_column(LargeBinary)
    tags: Mapped[list] = mapped_column(ARRAY(VARCHAR))
    content: Mapped[str] = mapped_column(TEXT)
    deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False)
   
    user_register = relationship('User', back_populates='document_register')
    log_document = relationship('LogDocument', back_populates='document', cascade='all, delete')
    
    def __repr__(self):
        return f'{self.id} | {self.type} | {self.id_register_user} | {self.register_date} | {self.img} | {self.tags} | {self.content}'
    
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


class OcrConfig(Base):
    __tablename__ = 'ocr_config'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    img: Mapped[str] = mapped_column(LargeBinary)
    rois: Mapped[list] = mapped_column(ARRAY(VARCHAR))

    def __repr__(self):
        return f'{self.id} | {self.name} | {self.img} | {self.rois}'
    
# Create tables on postgre
if __name__ == '__main__':
    Base.metadata.create_all(engine)
