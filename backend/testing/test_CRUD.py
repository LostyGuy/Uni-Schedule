import pytest
import backend.CRUD as CRUD
import testing.test_database as db
import backend.models as models

from fastapi import Depends

db_conn = Depends(db.get_db)

def test_is_user_in_database():
    raise NotImplementedError

def test_new_user_register():
    new_user = models.user_login_credentials(
        email = 'johndoe@mail.com',
        hashed_password = 'to_be_hashed',
        policy_agreement = True,
        role = 'user',
    )
    db.commit(new_user)
    user_query = db_conn.query(
        models.user_login_credentials.id,
        models.user_login_credentials.email,
        models.user_login_credentials.hashed_password,
        models.user_login_credentials.policy_agreement,
    ).one_or_none().limit(1)

    assert user_query['id'] == 0
    assert user_query['email'] == new_user.email
    assert user_query['hashed_password'] == new_user.hashed_password
    assert user_query['policy_agreement'] == new_user.policy_agreement

    db.rollback()

def test_user_login():
    raise NotImplementedError

def test_is_session_active():
    raise NotImplementedError

def test_user_logout():
    raise NotImplementedError

def test_get_user_profile():
    raise NotImplementedError