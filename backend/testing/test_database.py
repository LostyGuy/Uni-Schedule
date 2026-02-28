from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"

Testengine = create_engine(DATABASE_URL)
TestSessionLocal = sessionmaker(bind=Testengine, autoflush=False, autocommit=False)

def get_db():
    Testdb = TestSessionLocal()
    try:
        yield Testdb
    finally:
        Testdb.close()