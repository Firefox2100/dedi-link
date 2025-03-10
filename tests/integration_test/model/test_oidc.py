import pytest
from dedi_link.model.oidc import OidcDriver


@pytest.fixture
def mock_oidc_driver():
    return OidcDriver(
        client_id='node1',
        client_secret='node_secret_1',
        discovery_url='http://localhost:5556/.well-known/openid-configuration',
    )


class TestOidcDriver:
    def test_init(self):
        driver = OidcDriver(
            client_id='node1',
            client_secret='node_secret_1',
            discovery_url='http://localhost:5556/.well-known/openid-configuration',
        )

        assert driver.oauth.client_id == 'node1'
        assert driver.oauth.client_secret == 'node_secret_1'
        assert driver._discovery_document['issuer'] == 'http://localhost:5556'

    def test_service_token(self, mock_oidc_driver):
        service_token = mock_oidc_driver.service_token

        assert service_token


