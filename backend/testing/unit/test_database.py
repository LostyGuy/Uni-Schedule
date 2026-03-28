import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Testengine = create_engine('postgresql://postgres:postgres@localhost:54322/postgres')
TestSessionLocal = sessionmaker(bind=Testengine, autoflush=False, autocommit=False)

def get_db():
    Testdb = TestSessionLocal()
    try:
        yield Testdb
    finally:
        Testdb.close()