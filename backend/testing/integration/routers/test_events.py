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


@pytest.mark.skip
def test_add_event_request(Client):
    raise NotImplementedError

@pytest.mark.skip
def test_delete_event_request(Client):
    raise NotImplementedError

@pytest.mark.skip
def test_change_event_request(Client):
    raise NotImplementedError