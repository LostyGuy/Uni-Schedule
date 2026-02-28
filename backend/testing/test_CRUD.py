import pytest
import backend.app.CRUD as CRUD
import backend.database.models as models
from backend.testing.test_database import Testengine, TestSessionLocal
from backend.database.database import Base
from backend.timestamps import current_time
from backend.logging import log_info
from backend.private_logic.hashing import algorithm, hash_salt, hashed_answer_1, hashed_answer_2, hashed_answer_3

#----Database and Session Setup----
@pytest.fixture(autouse=True)
def database_setup():
    Base.metadata.drop_all(bind=Testengine)
    Base.metadata.create_all(bind=Testengine)
    session = TestSessionLocal()
    try:
        admin_role = models.role(
            name = 'owner',
            description = 'none',
        )
        user_role = models.role(
            name = 'user',
            description = 'none',
        )
        session.add_all([admin_role, user_role])
        session.commit()
    except Exception as e:
        log_info(e)
    yield
    session.close()
    Base.metadata.drop_all(bind=Testengine)

@pytest.fixture
def db_session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

#----Tests----
def test_is_user_in_database():
    raise NotImplementedError

def test_new_user_register(db_session):
    new_user_credentials: dict[str:str] = {
        'email': 'johndoe@mail.com',
        'password': 'to_be_hashed',
        'created_at': current_time(),
        'policy_agreement': True,
        'lastly_signed_in_on': current_time(),
        'role': 2,
    }

    CRUD.new_user_register(
        email = new_user_credentials['email'],
        password = new_user_credentials['password'],
        policy_agreement = new_user_credentials['policy_agreement'],
        role = new_user_credentials['role'],
        db_session = db_session,
    )

    user_query = db_session.query(
            models.user_login_credentials.id,
            models.user_login_credentials.email,
            models.user_login_credentials.hashed_password,
            models.user_login_credentials.policy_agreement,
        ).limit(1).one_or_none()

    assert user_query is not None
    assert user_query.email == new_user_credentials['email']
    assert user_query.hashed_password == new_user_credentials['password']
    assert user_query.policy_agreement == new_user_credentials['policy_agreement']

def test_hashing():
    assert CRUD.hash_password('Dog', algorithm, hash_salt) == hashed_answer_1
    assert CRUD.hash_password('Youve_seen_nothing_like124876', algorithm, hash_salt) == hashed_answer_2
    assert CRUD.hash_password('Te$t_of$pec!@l_S!gn$', algorithm, hash_salt) == hashed_answer_3

def test_user_login():
    raise NotImplementedError

def test_is_session_active():
    raise NotImplementedError

def test_user_logout():
    raise NotImplementedError

def test_get_user_profile():
    raise NotImplementedError