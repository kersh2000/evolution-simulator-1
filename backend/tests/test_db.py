# Define a function to delete the SQLite test database using SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..src.db.db import Base
from ..src.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # Create tables for our test

def get_user(db_session, username):
    return db_session.query(User).filter(User.username == username).first()

def test_create_user():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    try:
        test_username = "test_user"
        test_email = "test@test.com"
        test_password = "test_pass"

        test_user = User(username=test_username, email=test_email, hashed_password=test_password)
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        db_user = get_user(session, test_username)
        assert db_user
        assert db_user.username == test_username
        assert db_user.email == test_email
        assert db_user.hashed_password == test_password

    finally:
        session.close()
        transaction.rollback()
        connection.close()
