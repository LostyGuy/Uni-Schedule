import pytest
from fastapi.testclient import TestClient
import backend.app.main as main
import backend.connection.connection as connection
import backend.testing.unit.test_database as Testdb

#!----Status Codes----
#   200 - OK
#   303 - See Other
#   404 - Error Found
#   405 - Method Not Allowed
#   500 - Internal Server Error

#----Mock DB Setup----
@pytest.fixture
def Client():
    main.app.dependency_overrides[connection.get_db] = Testdb.get_db
    return TestClient(main.app)

#----User Related----
def test_user_login_request(Client):
    result = Client.post("/login_request", json={
        "username":"JohnDoe", 
        "email":"johndoe@mail.jd",
        "password":"JohnDoePass",
        "policy_agreement": True,
        })

    assert result.status_code == 200
    list_of_variables: list[str] = (
        "username",
        "access_token",
        "issued_at",
        "valid_till",
        )
    for variable in list_of_variables:
        assert variable in result.json()

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