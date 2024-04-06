from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database connection will fail if the script is not being ran in the parent directory (/backend)
load_dotenv('../../app/.env')

database_hostname = os.getenv('DB_HOSTNAME')
database_name = os.getenv('DB_NAME')
database_password = os.getenv('DB_PASSWORD')
database_username = os.getenv('DB_USERNAME')

SQLALCHEMY_DB_URL = f"postgresql://{database_username}:{database_password}@{database_hostname}/{database_name}"

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()