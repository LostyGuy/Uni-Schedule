import pytest
import backend.app.user_related.user_CRUD as user_CRUD
import backend.database.models as models
from backend.testing.test_database import Testengine, TestSessionLocal
from backend.database.database import Base
from backend.timestamps import current_time
from backend.logging import log_info_test_space, current_function
from backend.private_logic.hashing import algorithm, hash_salt, hashed_answer_1, hashed_answer_2, hashed_answer_3 # type: ignore
from backend.private_logic.jwt import TOKEN_LIFESPAN
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


def role_for_setup() -> list[dict]:
    admin_role = models.role(
        name = 'owner',
        description = 'none',
    )
    user_role = models.role(
        name = 'user',
        description = 'none',
    )
    return admin_role, user_role
        

def user_credential_for_setup() -> list[dict]:
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
    #----Add users to the database----
    test_new_user_register(db_session)
    #----Check if you can insert the same user twice----
    for user in user_credential_for_setup():
        try:
            result = user_CRUD.new_user_register(
                username = user['username'],
                email = user['email'],
                password = user['password'],
                policy_agreement = user['policy_agreement'],
                role = user['role'],
                db_session = db_session,
            )
        except Exception as e:
            log_info_test_space(current_function, e)
        if user['policy_agreement']:
            assert result == True
        else:
            assert result == False

def test_new_user_register(db_session):
    users = user_credential_for_setup()
    
    for new_user_credentials in users:
        result = user_CRUD.new_user_register(
            username = new_user_credentials['username'],
            email = new_user_credentials['email'],
            password = new_user_credentials['password'],
            policy_agreement = new_user_credentials['policy_agreement'],
            role = new_user_credentials['role'],
            db_session = db_session,
        )
        if new_user_credentials['policy_agreement']:
            assert result == True
        elif not new_user_credentials['policy_agreement']:
            assert result == False

def test_hashing():
    assert user_CRUD.hash_password('Dog', hash_salt) == hashed_answer_1
    assert user_CRUD.hash_password('Youve_seen_nothing_like124876', hash_salt) == hashed_answer_2
    assert user_CRUD.hash_password('Te$t_of$pec!@l_S!gn$', hash_salt) == hashed_answer_3

def test_user_login(db_session):
    #----Create Users----
    users = user_credential_for_setup()
    for user_credentials in users:
        user_CRUD.new_user_register(
            username = user_credentials['username'],
            email = user_credentials['email'],
            password = user_credentials['password'],
            policy_agreement = user_credentials['policy_agreement'],
            role = user_credentials['role'],
            db_session = db_session
        )
    #----Check Login----
        result = user_CRUD.user_login(
            email = user_credentials['email'],
            hashed_password = user_CRUD.hash_password(user_credentials['password'], hash_salt),
            db_session = db_session,
        )
        if user_credentials['policy_agreement']:
            assert result == True
        elif not user_credentials['policy_agreement']:
            assert result == False

def test_user_logout():
    raise NotImplementedError

def test_get_user_profile():
    raise NotImplementedError