# db/initialize_db.py
from db.db import engine
from models.user import Base  # Import Base from the user_model module

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
