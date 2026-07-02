import os

import pytest

import backend.app.services.v1 as v1
import backend.connection.models as models
from backend.testing.conftest import users_data, roles_data
from backend.security.hashing import hash_string
from backend.logging import log_error


#!----Tests----

def test_new_user_register(db_session):
    '''This test takes user data and puts it into CRUD to register the user into system'''

    register_Emily = v1.user_CRUD.user_register(
        name= 'Emily',
        surname= 'Mayer',
        username= 'EmilyMayer',
        email= 'emilyheartbreaker@mail.to',
        password= 'my_heart_is_broken',
        policy_agreement= True,
        db_session= db_session,
    )
    assert register_Emily


def test_user_login(db_session):
    """
    Verify that user login authentication creates an access token and corresponding login session record.
    """
    
    user_credentials = [
            {
            "email": "johndoe@mail.com",
            "password": "to_be_hashed",
            "device_name": "windows10",
            "ip_address": "255.255.255.254",
        }, #!---- User Exists ----
            {
            "email": "john.lemon@gmail.com",
            "password": "heheNOPE1",
            "device_name": "windows11",
            "ip_address": "255.255.255.255",
        } #!---- User Do NOT Exists ----
    ]

    for index, user in enumerate(user_credentials):

        try:
            token = v1.user_login(
                email= user.get("email"),
                password= user.get("password"),
                device_name= user.get("device_name"),
                ip_address= user.get("ip_address"),
                db_session= db_session,
            )
        except Exception as e:
            log_error("v1_user_login: ", e)
            raise RuntimeError

        if index == 0 and token:
            assert token != {}
            
        elif index == 1 and token:
            assert token.get("access_token") is None and token.get("refresh_token") is None

        else:
            log_error("Unknown index appeared")
            raise RuntimeError

@pytest.mark.skip
def test_user_logout(db_session):
    ''' BAD '''

    #----Log In----
    for user in users_data():
        success, access_token = v1.user_CRUD.user_login(
            email= user.email,
            hashed_password= user.hashed_password,
            db_session= db_session,
        )

        assert success == True
    #----Log Out----
        result = v1.user_CRUD.user_log_out(
            access_token= access_token,
            db_session= db_session
        )
        status: list[any] = db_session.query(
        models.login_session.status,
        ).filter(
            models.refresh_tokens.User_session.acess_token == access_token,
        ).order_by(
            models.refresh_tokens.User_session.issued_at.desc()
        ).first()

        assert result == True
        assert status[0] == 'Revoked'
        
#!---Suspended for now----
# def test_get_user_profile():
#   pass