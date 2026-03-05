import pytest
import backend.app.user_related.user_CRUD as user_CRUD
import backend.database.models as models
from backend.testing.test_database import Testengine, TestSessionLocal
from backend.database.database import Base
from backend.timestamps import current_time
from backend.logging import log_info_test_space, current_function
from backend.private_logic.hashing import algorithm, hash_salt, hashed_answer_1, hashed_answer_2, hashed_answer_3 # type: ignore
from backend.security.jwt_tokens import jwt_validation
from typing import Annotated

#----Database and Session Setup----
@pytest.fixture(autouse=True)
def database_setup():
    Base.metadata.drop_all(bind=Testengine)
    Base.metadata.create_all(bind=Testengine)
    session = TestSessionLocal()
    try:
        admin_role, user_role = role_for_setup()
        session.add_all([admin_role, user_role])
        session.commit()
    except Exception as e:
        log_info_test_space(current_function, e)
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

def role_for_setup() -> {dict, dict}:
    admin_role = models.role(
        name = 'owner',
        description = 'none',
    )
    user_role = models.role(
        name = 'user',
        description = 'none',
    )
    return admin_role, user_role
        

def user_credential_for_setup() -> {dict, dict, dict, dict}:
    """Arguments in users: 
        username, 
        email, 
        password, 
        created_at, 
        policy_agreement, 
        lastly_signed_in_on, 
        role,
    """
    
    new_user_John: dict[str:str] = {
        'username': 'Havent seen anything',
        'email': 'johndoe@mail.com',
        'password': 'to_be_hashed',
        'created_at': current_time(),
        'policy_agreement': True,
        'lastly_signed_in_on': current_time(),
        'role': 2,
    }
    new_user_Tom: dict[str:str] = {
            'username': 'tom',
            'email': 'tomprince@mail.com',
            'password': '$ome_cr@zy_p@$$',
            'created_at': current_time(),
            'policy_agreement': True,
            'lastly_signed_in_on': current_time(),
            'role': 2,
    }
    new_user_Anna: dict[str:str] = {
            'username': 'anna321498',
            'email': 'annacatlover313452@mail.com',
            'password': 'no!_$ome_cr@zy_p@$$',
            'created_at': current_time(),
            'policy_agreement': False,
            'lastly_signed_in_on': current_time(),
            'role': 2,
    }
    new_user_Max: dict[str:str] = {
            'username': 'Definitive',
            'email': 'atheobserverof@mail.com',
            'password': '1234',
            'created_at': current_time(),
            'policy_agreement': True,
            'lastly_signed_in_on': current_time(),
            'role': 1,
    }
    return new_user_John, new_user_Tom, new_user_Anna, new_user_Max

#----Tests----
def test_is_user_in_database(db_session):
    n_users= 3
    #----Add users to the database----
    test_new_user_register(db_session, n_users= n_users)
    #----Check if you can insert the same user twice----
    for user in user_credential_for_setup()[0:n_users-1]:
        try:
            user_CRUD.new_user_register(
                username = user['username'],
                email = user['email'],
                password = user['password'],
                policy_agreement = user['policy_agreement'],
                role = user['role'],
                db_session = db_session,
            )
        except Exception as e:
            log_info_test_space(current_function, e)
        finally:
            assert e is not None

def test_new_user_register(db_session: None, n_users: int):
    n_users=4
    # new_user_credentials: dict[str:str] = {
    #     'email': 'johndoe@mail.com',
    #     'password': 'to_be_hashed',
    #     'created_at': current_time(),
    #     'policy_agreement': True,
    #     'lastly_signed_in_on': current_time(),
    #     'role': 2,
    # }
    users = user_credential_for_setup()

    for new_user_credentials in users[0:n_users-1]:
        user_CRUD.new_user_register(
            username = new_user_credentials['username'],
            email = new_user_credentials['email'],
            password = new_user_credentials['password'],
            policy_agreement = new_user_credentials['policy_agreement'],
            role = new_user_credentials['role'],
            db_session = db_session,
        )

        user_query = db_session.query(
                models.user_login_credentials.id,
                models.user_login_credentials.username,
                models.user_login_credentials.email,
                models.user_login_credentials.hashed_password,
                models.user_login_credentials.policy_agreement,
            ).filter(
                models.user_login_credentials.username == new_user_credentials['username'],
                models.user_login_credentials.email == new_user_credentials['email'],
                models.user_login_credentials.policy_agreement == new_user_credentials['policy_agreement'],
                models.user_login_credentials.role == new_user_credentials['role'],
            ).limit(1).one_or_none()

        if new_user_credentials['policy_agreement']:
            assert user_query is not None
        else:
            assert user_query is None
        

def test_hashing():
    assert user_CRUD.hash_password('Dog', algorithm, hash_salt) == hashed_answer_1
    assert user_CRUD.hash_password('Youve_seen_nothing_like124876', algorithm, hash_salt) == hashed_answer_2
    assert user_CRUD.hash_password('Te$t_of$pec!@l_S!gn$', algorithm, hash_salt) == hashed_answer_3

def test_user_login():
    n_users = 4
    users = user_credential_for_setup()

    for user_credentials in users[0:n_users-1]:
        result = user_CRUD.user_login(
            email = user_credentials['email'],
            hashed_password = user_credentials['hashed_password'],
        )
        payload = jwt_validation(result)
        assert 'user_id' in payload
        assert 'issued_at' in payload
        assert 'valid_till' in payload
        

def test_is_session_active():
    raise NotImplementedError

def test_user_logout():
    raise NotImplementedError

def test_get_user_profile():
    raise NotImplementedError