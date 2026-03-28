import pytest
import backend.app.user.user_CRUD as user_CRUD
import backend.connection.models as models
from backend.connection.connection import Base
from backend.timestamps import current_time
from backend.logging import log_info_test_space, current_function
# from backend.database.database import SessionLocal, engine

from backend.testing.unit.test_database import Testengine, TestSessionLocal
from backend.private_logic.hashing import algorithm, hash_salt, hashed_answer_1, hashed_answer_2, hashed_answer_3 # type: ignore
from backend.private_logic.jwt import TOKEN_LIFESPAN

from backend.security.jwt_tokens import jwt_validation
from typing import Annotated

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
        transaction.commit()
        connection.close()

@pytest.fixture(autouse=True)
def database_setup(db_session):
    users = users_credentials_for_setup()
    roles = roles_for_setup()
    db_session.add_all(roles)
    db_session.flush()
    db_session.add_all(users)
    db_session.flush()
    

def roles_for_setup() -> list[dict]:
    admin_role = models.role(
        role_id = 1,
        name = 'owner',
        description = 'none',
    )
    user_role = models.role(
        role_id = 2,
        name = 'user',
        description = 'none',
    )
    return admin_role, user_role
        
def users_credentials_for_setup() -> list[dict]:
    """Arguments in users: 
        username, 
        email, 
        password, 
        created_at, 
        policy_agreement, 
        lastly_signed_in_on, 
        role,
    """
    
    new_user_John = models.user_login_credentials(
        username = 'Havent seen anything',
        email = 'johndoe@mail.com',
        hashed_password = user_CRUD.hash_password('to_be_hashed', hash_salt),
        created_at = current_time(),
        policy_agreement = True,
        lastly_signed_in_on = current_time(),
        role = 2,
    )
    new_user_Tom = models.user_login_credentials(
        username = 'tom',
        email = 'tomprince@mail.com',
        hashed_password = user_CRUD.hash_password('$ome_cr@zy_p@$$', hash_salt),
        created_at = current_time(),
        policy_agreement = True,
        lastly_signed_in_on = current_time(),
        role = 2,
    )
    new_user_Anna = models.user_login_credentials(
        username = 'anna321498',
        email = 'annacatlover313452@mail.com',
        hashed_password = user_CRUD.hash_password('no!_$ome_cr@zy_p@$$', hash_salt),
        created_at = current_time(),
        policy_agreement = True,
        lastly_signed_in_on = current_time(),
        role = 2,   
    )
    new_user_Max = models.user_login_credentials(
        username = 'Definitive',
        email = 'atheobserverof@mail.com',
        hashed_password = user_CRUD.hash_password('1234', hash_salt),
        created_at = current_time(),
        policy_agreement = True,
        lastly_signed_in_on = current_time(),
        role = 1,
    )
    return new_user_John, new_user_Tom, new_user_Anna, new_user_Max

#!----Tests----
def test_is_user_in_database(db_session):
    '''This test determines if the above setup is correct'''

    for user in users_credentials_for_setup():
        try:
            result = db_session.query(
                models.user_login_credentials.username,
                models.user_login_credentials.email,
                models.user_login_credentials.policy_agreement,
            ).filter(models.user_login_credentials.username == user.username).first()
            log_info_test_space(current_function, user.username)
        except Exception as e:
            log_info_test_space(current_function, e)
        log_info_test_space(current_function, result)
        if result:
            assert result is not None
            assert user.username == result[0]
            assert user.email == result[1]
            assert user.policy_agreement == result[2]
        else:
            assert result is None

def test_new_user_register(db_session):
    '''This test takes user data and puts it into CRUD to register the user into system'''

    register_Emily = user_CRUD.new_user_register(
        username = 'EmilyMayer',
        email = 'emilyheartbreaker@mail.to',
        password = 'my_heart_is_broken',
        policy_agreement = True,
        db_session = db_session,
    )
    assert register_Emily == True

def test_hashing():
    assert user_CRUD.hash_password('Dog', hash_salt) == hashed_answer_1
    assert user_CRUD.hash_password('Youve_seen_nothing_like124876', hash_salt) == hashed_answer_2
    assert user_CRUD.hash_password('Te$t_of$pec!@l_S!gn$', hash_salt) == hashed_answer_3

def test_user_login(db_session):
    ''' '''
    #----Check Login----
    for user in users_credentials_for_setup():
        login_result = user_CRUD.user_login(
            email= user.email,
            hashed_password= user.hashed_password,
            db_session= db_session,
        )
    #----Check if access token was created----
        if login_result[0] == False:
            break
        elif login_result[1] is not None:
            assert login_result[0] == True

        session_result = db_session.query(
            models.login_session.id
        ).filter(models.login_session.access_token == login_result[1]).first()

        assert session_result is not None
    #----Check Cookie----

def test_user_logout(db_session):
    ''' '''

    #----Log In----
    for user in users_credentials_for_setup():
        success, access_token = user_CRUD.user_login(
            email= user.email,
            hashed_password= user.hashed_password,
            db_session= db_session,
        )

        assert success == True
    #----Log Out----
        result = user_CRUD.user_log_out(
            access_token= access_token,
            db_session= db_session
        )
        status: list[any] = db_session.query(
        models.login_session.status,
        ).filter(
            models.login_session.access_token == access_token,
        ).order_by(
            models.login_session.issued_at.desc()
        ).first()

        assert result == True
        assert status[0] == 'Revoked'
        
#!---Suspended for now----
# def test_get_user_profile():
#   pass