"""
OIDC integrated driver for access token management and validation
"""

from httpx import Client
from authlib.integrations.requests_client import OAuth2Session


class OidcDriver:
    """
    OIDC integrated driver for access token management and validation
    """
    def __init__(self,
                 driver_id: str,
                 client_id: str,
                 client_secret: str,
                 discovery_url: str,
                 ):
        """
        Initialize OIDC driver

        :param client_id: Client ID
        :param client_secret: Client secret
        :param discovery_url: OIDC discovery URL
        """
        self.driver_id = driver_id

        with Client() as client:
            response = client.get(discovery_url)
            response.raise_for_status()
            self._discovery_document = response.json()

        self.oauth = OAuth2Session(
            client_id=client_id,
            client_secret=client_secret,
        )

    @property
    def service_token(self):
        """
        Get access token for service account with client credentials grant type

        :return:
        """
        token_response = self.oauth.fetch_token(
            url=self._discovery_document['token_endpoint'],
            grant_type='client_credentials',
            client_id=self.oauth.client_id,
            client_secret=self.oauth.client_secret,
        )

        return token_response['access_token']

    def introspect_token(self, token: str):
        """
        Introspect an access token

        :param token: Access token to introspect
        :return: Introspection response
        """
        introspect_response = self.oauth.introspect_token(
            url=self._discovery_document['introspection_endpoint'],
            token=token,
        )

        return introspect_response.json()


class OidcRegistry:
    """
    OIDC driver registry
    """
    def __init__(self):
        self._drivers = {}
        self._default_driver = None

    def __getitem__(self, item) -> OidcDriver:
        return self._drivers[item]

    @property
    def default_driver(self) -> OidcDriver:
        if self._default_driver is None:
            raise RuntimeError('OIDC registry is empty')

        return self._default_driver

    @property
    def service_token(self):
        """
        Get access token for service account with client credentials grant type

        :return:
        """
        return self._default_driver.service_token

    def register_driver(self,
                        driver: OidcDriver,
                        is_default: bool = False,
                        ):
        """
        Register an OIDC driver

        :param driver: OIDC driver
        :param is_default: Whether to set this driver as the default driver
        """
        self._drivers[driver.driver_id] = driver

        if self._default_driver is None or is_default:
            self._default_driver = driver

    def introspect_token(self,
                         token: str,
                         driver_id: str = None,
                         ) -> dict:
        """
        Introspect an access token

        :param driver_id: Driver ID
        :param token: Access token to introspect
        """
        if driver_id is None:
            if self._default_driver is None:
                raise RuntimeError('OIDC registry is empty')

            return self._default_driver.introspect_token(token)

        try:
            return self._drivers[driver_id].introspect_token(token)
        except KeyError:
            raise ValueError(f'Driver {driver_id} not found in registry')
