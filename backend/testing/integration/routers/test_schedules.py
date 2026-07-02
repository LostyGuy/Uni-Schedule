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

#----Schedule Related----
@pytest.mark.skip
def test_create_schedule_request(Client):
    raise NotImplementedError

@pytest.mark.skip
def test_delete_schedule_request(Client):
    raise NotImplementedError

@pytest.mark.skip
def test_change_schedule_request(Client):
    raise NotImplementedError