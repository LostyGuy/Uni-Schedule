import pytest
from sqlalchemy import select
import secrets

import backend.connection.models as models
import backend.security.tokens as token
from backend.security.hashing import hash_string
from backend.logging import log_error
from backend.testing.conftest import EXISTING_USERS
from backend.timestamps import current_time


def test_create_refresh_token(db_session):
    
    try:
        user_id = db_session.execute(
            select(
                models.User.user_id
            ).where(
                models.User.email == EXISTING_USERS[0]["email"],
                models.User.hashed_password == hash_string(EXISTING_USERS[0]["password"])
            )
        ).scalar_one()
    except Exception as e:
        log_error("Test_Create_Refresh_Token: ", e)
        assert True == False #-- Force error --
    
    raw_token = token.create_refresh_token(
        user_id = user_id,
        device_name= EXISTING_USERS[0]["device_name"],
        ip_address= EXISTING_USERS[0]["ip_address"],
        db_session=db_session,
    )
    
    assert raw_token != None
    
    
def test_update_refresh_token(db_session):
    
    old_raw_token: str = secrets.token_urlsafe(64)
    token_hash: str = hash_string(old_raw_token)
    
    Toms_id = db_session.execute(
        select(
            models.User.user_id
        ).where(
            models.User.email == "tomprince@mail.com"
        )
    ).scalar_one()
    
    # place hashed token in DB
    dummy_token = models.RefreshToken(
        user_id = Toms_id,
        token_hash = token_hash,
        expire_at = current_time() + token.REFRESH_LIFESPAN,
        ip_address = "10.10.10.10",
    )
    db_session.add(dummy_token)
    db_session.commit()
    
    
    new_raw_token = token.update_refresh_token(
        raw_token=old_raw_token,
        db_session=db_session,
    )
    is_Tom_an_owner = db_session.execute(
        select(
            models.RefreshToken.user_id
        ).where(
            models.RefreshToken.token_hash == hash_string(new_raw_token),
            models.RefreshToken.ip_address == "10.10.10.10",
        )
    ).scalar_one()
    
    old_refresh_token = db_session.execute(
        select(
            models.RefreshToken.is_revoked
        ).where(
            models.RefreshToken.token_hash == hash_string(old_raw_token)
        )
    ).scalar_one()
    
    assert Toms_id == is_Tom_an_owner
    assert old_refresh_token == True
    assert old_raw_token != new_raw_token    
    

@pytest.mark.skip
def test_revoke_refresh_token(db_session):
    raise NotImplementedError

@pytest.mark.skip
def test_revoke_all_refresh_tokens(db_session):
    raise NotImplementedError

@pytest.mark.skip
def test_create_access_token(db_session):
    raise NotImplementedError

@pytest.mark.skip
def test_on_password_change(db_session):
    raise NotImplementedError