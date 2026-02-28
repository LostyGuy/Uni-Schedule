from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.database import Base

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

Testengine = create_engine(DATABASE_URL)
TestSessionLocal = sessionmaker(bind=Testengine, autoflush=False, autocommit=False)
TestBase = declarative_base()

Base.metadata.create_all(bind=Testengine)

def get_db():
    Testdb = TestSessionLocal()
    try:
        yield Testdb
    finally:
        Testdb.close()