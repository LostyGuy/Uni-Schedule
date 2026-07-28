import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.connection.connection import Base, get_db
import backend.connection.models as models
from backend.security.hashing import hash_string

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:15432/postgres"

engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

try:
    with engine.connect() as conn:
        pass
except OperationalError:
    pytest.exit(
        "Test database unreachable. Is Supabase Docker running? → supabase start",
        returncode=1
    )


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        roles = roles_data()
        users = users_data()
        session.add_all(roles)
        session.add_all(users)
        session.commit()
        yield
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine, tables=reversed(Base.metadata.sorted_tables))


@pytest.fixture
def db_session(setup_db):
    with engine.begin() as connection:
        session = TestSessionLocal(bind=connection)
        yield session
        session.close()
        connection.rollback()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def users_data() -> list[dict]:
    """
    Create test user records for database seeding in unit tests.
    
    Returns:
        A tuple of two user model instances with test credentials and hashed passwords.
    """
    new_user_John = models.users.User(
        name= 'John',
        surname= 'Doe',
        username= 'Havent seen anything',
        email= 'johndoe@mail.com',
        hashed_password= hash_string('to_be_hashed'),
        role_id= 2,
        policy_agreement= True,
        
    )
    new_user_Tom = models.users.User(
        name= 'Tom',
        surname= 'Prince',
        username= 'tom',
        email= 'tomprince@mail.com',
        hashed_password= hash_string('$ome_cr@zy_p@$$'),
        role_id= 2,
        policy_agreement= True,
    )
    return [new_user_John, new_user_Tom]


def roles_data() -> list[dict]:
    """
    Create and return role objects for test database seeding.
    
    Returns two predefined roles: an 'owner' role with ID 1 and a 'user' role with ID 2.
    
    Returns:
    	tuple: A tuple containing two models.roles objects (owner_role, user_role)
    """
    admin_role = models.auth.Role(
        role_id= 1,
        name= 'owner',
        description= 'none',
        can_manage_events= True,
        can_invite_members= True,
    )
    user_role = models.auth.Role(
        role_id= 2,
        name= 'user',
        description= 'none',
        can_manage_events= False,
        can_invite_members= False,
    )
    return [admin_role, user_role]
