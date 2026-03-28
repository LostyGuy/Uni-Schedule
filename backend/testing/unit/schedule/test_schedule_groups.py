import pytest
from backend.testing.unit.test_database import Testengine, TestSessionLocal


#----Database and Session Setup----
@pytest.fixture
def db_session():
    connection = Testengine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    session.begin_nested()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

#!----Tests----

#----Groups----
def test_create_group():
    raise NotImplementedError

def test_remove_group():
    raise NotImplementedError

def test_join_group():
    raise NotImplementedError

def test_leave_group():
    raise NotImplementedError

def test_remove_user_from_group():
    raise NotImplementedError


#----Group Permission----
def test_grant_editing_on_group_schedule():
    raise NotImplementedError

def test_revoke_editing_on_group_schedule():
    raise NotImplementedError


#----Group Invitation----
def test_generate_join_QRcode():
    raise NotImplementedError

def test_generate_join_url():
    raise NotImplementedError