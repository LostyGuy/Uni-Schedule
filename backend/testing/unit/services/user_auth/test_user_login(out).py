import os

import pytest
from sqlalchemy import select

import backend.app.services.v1 as v1
import backend.connection.models as models
from backend.testing.conftest import MIXED_USERS
from backend.logging import log_error
from backend.security.tokens import create_refresh_token
from backend.security.hashing import hash_string


def test_user_login(db_session):
    """
    Verify that user login authentication creates an access token and corresponding login session record.
    """
    
    # user_credentials = [
    #         {
    #         "email": "johndoe@mail.com",
    #         "password": "to_be_hashed",
    #         "device_name": "windows10",
    #         "ip_address": "255.255.255.254",
    #     }, #!---- User Exists ----
    #         {
    #         "email": "john.lemon@gmail.com",
    #         "password": "heheNOPE1",
    #         "device_name": "windows11",
    #         "ip_address": "255.255.255.255",
    #     } #!---- User Does NOT Exist ----
    # ]

    for index, user in enumerate(MIXED_USERS):

        try:
            token = v1.user_login(
                email= user["email"],
                password= user["password"],
                device_name= user["device_name"],
                ip_address= user["ip_address"],
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


def test_user_logout(db_session):
    '''  '''
    user_id = db_session.scalar(
        select(
            models.User.user_id,
        ).where(
            models.User.email == "johndoe@mail.com",
        )
    )

    assert user_id is not None

    raw_token = create_refresh_token(
        user_id= user_id,
        device_name= "testOS",
        ip_address= "255.255.255.254",
        db_session= db_session,
    )

    success = v1.user_log_out(db_session, raw_token)
    assert success is True
    
    stmt = select(
            models.RefreshToken,
        ).where(
            models.RefreshToken.token_hash == hash_string(raw_token),
        )
    
    token_row = db_session.scalars(stmt).one_or_none()
    assert token_row.is_revoked is True