from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.database import engine
from app import models

def check_and_create_users_table():
    # Create a new session
    session = Session(bind=engine)
    try:
        # Use the inspector to check if the users table exists
        inspector = inspect(engine)
        if not inspector.has_table("users"):
            print("Users table does not exist. Creating table...")
            # Create the users table
            models.Base.metadata.create_all(bind=engine, tables=[models.User.__table__])
            print("Users table created successfully.")
        else:
            print("Users table already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_and_create_users_table()
