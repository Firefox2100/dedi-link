import secrets
import pytest
from Cryptodome.PublicKey import RSA
from jwkest.jwk import RSAKey
from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.subject_identifier import HashBasedSubjectIdentifierFactory
from pyop.userinfo import Userinfo


@pytest.fixture
def mock_oidc_signing_key():
    rsa_keys = RSA.generate(4096)

    jwk = RSAKey(
        kid='test',
        key=rsa_keys,
    )

    return jwk


@pytest.fixture
def mock_oidc_user_db():
    return {}


@pytest.fixture
def mock_oidc_clients():
    return {}


@pytest.fixture
def mock_oidc_provider(mock_oidc_signing_key,
                       mock_oidc_user_db,
                       mock_oidc_clients,
                       ):
    hash_salt = secrets.token_urlsafe(16)[:16]
    base_url = 'https://mock-op.local'

    config_info = {
        'issuer': base_url,
        'authorization_endpoint': f'{base_url}/authentication',
        'jwks_uri': f'{base_url}/jwks',
        'token_endpoint': f'{base_url}/token',
        'userinfo_endpoint': f'{base_url}/userinfo',
        'registration_endpoint': f'{base_url}/registration',
        'end_session_endpoint': f'{base_url}/logout',
        'scopes_supported': ['openid', 'profile'],
        'response_types_supported': ['code', 'code id_token', 'code token', 'code id_token token'],  # code and hybrid
        'response_modes_supported': ['query', 'fragment'],
        'grant_types_supported': ['authorization_code', 'implicit'],
        'subject_types_supported': ['pairwise'],
        'token_endpoint_auth_methods_supported': ['client_secret_basic'],
        'claims_parameter_supported': True
    }
    user_info = Userinfo(mock_oidc_user_db)

    provider = Provider(
        signing_key=mock_oidc_signing_key,
        configuration_information=config_info,
        authz_state=AuthorizationState(
            subject_identifier_factory=HashBasedSubjectIdentifierFactory(
                hash_salt=hash_salt,
            ),
        ),
        clients=mock_oidc_clients,
        userinfo=user_info,
    )

    return provider
