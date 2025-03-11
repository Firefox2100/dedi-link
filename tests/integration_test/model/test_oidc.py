import pytest
from httpx import Client

from dedi_link.model.oidc import OidcDriver


@pytest.fixture
def mock_oidc_driver():
    return OidcDriver(
        driver_id='http://localhost:5556',
        client_id='node1',
        client_secret='node_secret_1',
        discovery_url='http://localhost:5556/.well-known/openid-configuration',
    )


class TestOidcDriver:
    def test_init(self):
        driver = OidcDriver(
            driver_id='http://localhost:5556',
            client_id='node1',
            client_secret='node_secret_1',
            discovery_url='http://localhost:5556/.well-known/openid-configuration',
        )

        assert driver.driver_id == 'http://localhost:5556'
        assert driver.oauth.client_id == 'node1'
        assert driver.oauth.client_secret == 'node_secret_1'
        assert driver._discovery_document['issuer'] == 'http://localhost:5556'

    def test_service_token(self, mock_oidc_driver):
        service_token = mock_oidc_driver.service_token

        assert service_token

    def test_introspect_token(self, mock_oidc_driver):
        username = 'MockUser1'
        password = 'mock_password_1'

        # Direct access grant to get the token
        with Client() as client:
            response = client.post(
                'http://localhost:5556/token',
                data={
                    'grant_type': 'password',
                    'client_id': 'node1',
                    'client_secret': 'node_secret_1',
                    'username': username,
                    'password': password,
                },
            )
            response.raise_for_status()
            token = response.json()['access_token']

        introspection_result = mock_oidc_driver.introspect_token(token)
