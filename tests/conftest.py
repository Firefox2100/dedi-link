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

    config_info = {}
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
