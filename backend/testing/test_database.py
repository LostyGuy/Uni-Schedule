import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.private_logic.database_url import TEST_DATABASE_URL

Testengine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=Testengine, autoflush=False, autocommit=False)

def get_db():
    Testdb = TestSessionLocal()
    try:
        yield Testdb
    finally:
        Testdb.close()