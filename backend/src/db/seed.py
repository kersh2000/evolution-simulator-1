# db/seed.py
from sqlalchemy.orm import sessionmaker
from db.db import engine
from models.user import User

def seed_db():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    # Add a check to prevent reseeding if there are already users in the DB
    if db.query(User).count() == 0:
        user_data = [
            {"username": "user1", "email": "user1@example.com", "hashed_password": "hash1"},
            {"username": "user2", "email": "user2@example.com", "hashed_password": "hash2"},
            # Add more users as needed
        ]

        for data in user_data:
            db_user = User(**data)
            db.add(db_user)
    
        db.commit()

if __name__ == "__main__":
    seed_db()
