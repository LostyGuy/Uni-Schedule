import pytest
from fastapi.testclient import TestClient

import backend.app.main as main
import backend.connection.connection as connection

#!----Status Codes----
#   200 - OK
#   303 - See Other
#   404 - Error Found
#   405 - Method Not Allowed
#   500 - Internal Server Error


#----Group Related----
@pytest.mark.skip
def test_create_invitation_request(Client):
    raise NotImplementedError

@pytest.mark.skip
def test_intivation_request(Client):
    raise NotImplementedError

@pytest.mark.skip
def test_leave_group_request(Client):
    raise NotImplementedError

#----Role Related----
@pytest.mark.skip
def test_grant_role_on_schedule_request(Client):
    raise NotImplementedError

@pytest.mark.skip
def test_revoke_role_on_schedule_request(Client):
    raise NotImplementedError

#TODO----Premium Related----
@pytest.mark.skip
def test_grant_premium_request():
    raise NotImplementedError

@pytest.mark.skip
def test_renew_premium_request():
    raise NotImplementedError