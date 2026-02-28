from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.private_logic.database_url import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()