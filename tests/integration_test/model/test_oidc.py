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
        username = 'user1@example.com'
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

        assert introspection_result['active'] is True
        assert introspection_result['sub'] == 'user1'
        assert introspection_result['client_id'] == 'node1'
        assert introspection_result['token_type'] == 'bearer'
        assert introspection_result['scope'] == 'openid profile email'
        assert introspection_result['exp'] is not None
        assert introspection_result['iat'] is not None
        assert 'node1' in introspection_result['aud']
        assert introspection_result['email'] == 'user1@example.com'
        assert introspection_result['username'] == 'user1@example.com'
