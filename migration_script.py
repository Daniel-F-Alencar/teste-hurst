import os
import sqlalchemy
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pymongo
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "default_fallback_url")
MONGO_CONNECTION = os.getenv("MONGO_CONNECTION", "default_fallback_url")

# Configuração do MongoDB
mongo_client = pymongo.MongoClient(MONGO_CONNECTION)
mongo_db = mongo_client["hurst_test_db"]
mongo_collection = mongo_db["account"]

# Configuração do banco de dados relacional (MySQL)
engine = create_engine(DATABASE_URL)
Base = sqlalchemy.orm.declarative_base()


# Definição das tabelas
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), unique=True)
    name = Column(String(100))
    email = Column(String(100))
    address = Column(String(200))
    date_of_birth = Column(DateTime)
    gender = Column(String(10))
    phone_number = Column(String(20))
    profile_picture = Column(String(200))
    account_status = Column(String(20))
    last_access = Column(DateTime)
    preferences = Column(Text)
    privacy_settings = Column(String(20))
    book_count = Column(Integer)
    registration_date = Column(DateTime)


class BankingDetail(Base):
    __tablename__ = "banking_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_number = Column(String(20))
    bank_name = Column(String(100))
    swift_code = Column(String(20))


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200))
    author = Column(String(100))
    isbn = Column(String(36))
    year = Column(Integer, nullable=True)


class UserBook(Base):
    __tablename__ = "userbooks"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)


# Criação das tabelas
Base.metadata.create_all(engine)

# Sessão
Session = sessionmaker(bind=engine)
session = Session()


# Função para converter string para datetime
def convert_to_datetime(value):
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    return value


# Migração dos dados
for account in mongo_collection.find():

    # Verificar se o usuário já existe no MySQL
    existing_user = session.query(User).filter_by(user_id=account["UserID"]).first()
    if existing_user:
        continue

    user = User(
        user_id=account["UserID"],
        name=account["Name"],
        email=account["Email"],
        address=account["Address"],
        date_of_birth=convert_to_datetime(account["DateOfBirth"]),
        gender=account["Gender"],
        phone_number=account["PhoneNumber"],
        profile_picture=account["ProfilePicture"],
        account_status=account["AccountStatus"],
        last_access=convert_to_datetime(account["LastAccess"]),
        preferences=account["Preferences"],
        privacy_settings=account["PrivacySettings"],
        book_count=account["BookCount"],
        registration_date=convert_to_datetime(account["RegistrationDate"]),
    )
    session.add(user)
    session.commit()

    # Migrando BankingDetails
    if "BankingDetails" in account:
        banking_details = BankingDetail(
            user_id=user.id,
            account_number=account["BankingDetails"].get("account_number"),
            bank_name=account["BankingDetails"].get("bank_name"),
            swift_code=account["BankingDetails"].get("swift_code"),
        )
        session.add(banking_details)
        session.commit()

    # Migrando Books
    for book_data in account["Books"]:
        book = session.query(Book).filter_by(isbn=book_data["ISBN"]).first()
        if not book:
            book = Book(
                title=book_data["Title"],
                author=book_data["Author"],
                isbn=book_data["ISBN"],
                year=book_data.get("Year"),
            )
            session.add(book)
            session.commit()

        user_book = UserBook(user_id=user.id, book_id=book.id)
        session.add(user_book)

    session.commit()
