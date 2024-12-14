"""
Test file to ensure mock OIDC provider is working
"""

import pytest

from pyop.authz_state import AuthorizationRequest


class TestOidcProvider:
    def test_auth_request_token(self,
                                mock_oidc_user_db,
                                mock_oidc_clients,
                                mock_oidc_provider,
                                ):
        mock_oidc_user_db['test_user'] = {
            'sub': 'test_user',
            'name': 'Test User',
            'email': 'test@mock-op.local',
        }

        mock_oidc_clients['test_client'] = {
            'client_id': 'test_client',
            'client_secret': 'test_secret',
            'redirect_uris': ['http://localhost:8000'],
            'response_types': ['code', 'code token', 'code id_token'],
            'grant_types': ['authorization_code', 'implicit'],
            'token_endpoint_auth_method': 'client_secret_post',
        }

        auth_req = AuthorizationRequest(
            client_id='test_client',
            redirect_uri='http://localhost:8000',
            response_type='code',
            scope='openid profile',
            state='test_state',
            nonce='test_nonce',
        )

        auth_response = mock_oidc_provider.authorize(
            authentication_request=auth_req,
            user_id='test_user',
        )

        assert auth_response['code'] is not None

        # Exchange the auth code with a token
        token_response = mock_oidc_provider.handle_token_request(
            request_body=(
                'grant_type=authorization_code&'
                f'code={auth_response["code"]}&'
                'redirect_uri=http%3A%2F%2Flocalhost%3A8000&'
                'client_id=test_client&'
                'client_secret=test_secret'
            ),
        )

        assert token_response['access_token'] is not None
