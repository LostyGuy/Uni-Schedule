import pytest
from fastapi.testclient import TestClient
import backend.core_logic as core_logic
import backend.db as db

#----Mock DB Setup----
@pytest.fixture
def Client():
    
    return TestClient(core_logic.app)

#----User Related----
def test_user_login_request(Client):
    raise NotImplementedError

def test_user_register_request(Client):
    raise NotImplementedError

def test_user_delete_request(Client):
    raise NotImplementedError

#----Schedule Related----
def test_create_schedule_request(Client):
    raise NotImplementedError

def test_delete_schedule_request(Client):
    raise NotImplementedError

def test_change_schedule_request(Client):
    raise NotImplementedError

#----Event Related----
def test_add_event_request(Client):
    raise NotImplementedError

def test_delete_event_request(Client):
    raise NotImplementedError

def test_change_event_request(Client):
    raise NotImplementedError

#----Group Related----
def test_create_group_request(Client):
    raise NotImplementedError

def test_delete_group_request(Client):
    raise NotImplementedError

def test_create_invitation_request(Client):
    raise NotImplementedError

def test_intivation_request(Client):
    raise NotImplementedError

def test_leave_group_request(Client):
    raise NotImplementedError

#----Role Related----
def test_grant_role_on_schedule_request(Client):
    raise NotImplementedError

def test_revoke_role_on_schedule_request(Client):
    raise NotImplementedError

#TODO----Premium Related----
def test_grant_premium_request():
    raise NotImplementedError

def test_renew_premium_request():
    raise NotImplementedError