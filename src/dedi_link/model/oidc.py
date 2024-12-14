from httpx import Client
from authlib.integrations.requests_client import OAuth2Session


class OidcDriver:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 discovery_url: str,
                 ):
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
            token_url=self._discovery_document['token_endpoint'],
            grant_type='client_credentials',
        )

        return token_response['access_token']

    def exchange_token(self, external_token: str):
        """
        Exchange a token from external IdP for a token from this IdP

        :param external_token: An access token from an external IdP.
        The external IdP must be configured in the IdP's trust relationships
        for identity brokering.
        :return: A token from this IdP
        """
        exchange_response = self.oauth.fetch_token(
            token_url=self._discovery_document['token_endpoint'],
            grant_type='urn:ietf:params:oauth:grant-type:token-exchange',
            subject_token=external_token,
            subject_token_type='urn:ietf:params:oauth:token-type:access_token',
        )

        return exchange_response['access_token']

    def introspect_token(self, token: str):
        """
        Introspect an access token

        :param token: Access token to introspect
        :return: Introspection response
        """
        introspect_response = self.oauth.fetch_token(
            token_url=self._discovery_document['introspection_endpoint'],
            grant_type='urn:ietf:params:oauth:grant-type:token-exchange',
            token=token,
        )

        return introspect_response
