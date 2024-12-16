import pytest
from unittest.mock import patch


@pytest.fixture
def mock_client():
    with patch('dedi_link.model.network_interface.session.httpx.Client') as mock_client:
        yield mock_client
