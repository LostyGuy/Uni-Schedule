from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://"

Testengine = create_engine(DATABASE_URL)
TestSessionLocal = sessionmaker(bind=Testengine, autoflush=False, autocommit = False)
TestBase = declarative_base()

def get_db():
    Testdb = TestSessionLocal()
    try:
        yield Testdb
    finally:
        Testdb.close()