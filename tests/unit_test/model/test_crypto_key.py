from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import rsa
import pytest

from dedi_link.model.crypto_key import Ec384PublicKey


class TestEc384PublicKey:
    def test_init(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()

        ec_key = Ec384PublicKey(public_key)
        assert ec_key.public_key.public_numbers() == public_key.public_numbers()

    def test_try_parse_valid_key(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        ec_key = Ec384PublicKey._try_parse(pem_public_key)
        assert ec_key.public_key.public_numbers() == public_key.public_numbers()

    def test_try_parse_invalid_key(self):
        invalid_pem = "-----BEGIN PUBLIC KEY-----\nINVALIDKEY\n-----END PUBLIC KEY-----"

        with pytest.raises(ValueError, match='Invalid public key format.'):
            Ec384PublicKey._try_parse(invalid_pem)

        invalid_value = 42

        with pytest.raises(TypeError, match='Public key must be a string in PEM format.'):
            Ec384PublicKey._try_parse(invalid_value)

    def test_try_parse_non_ecdsa_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        with pytest.raises(ValueError, match='The provided key is not an ECDSA public key.'):
            Ec384PublicKey._try_parse(pem_public_key)

    def test_try_parse_wrong_curve(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP256R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        with pytest.raises(ValueError, match='The ECDSA public key must use the NIST P-384 curve.'):
            Ec384PublicKey._try_parse(pem_public_key)

    def test_try_serialise(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        ec_key = Ec384PublicKey(public_key)
        serialized_pem = Ec384PublicKey._try_serialise(ec_key)
        assert serialized_pem == pem_public_key

    def test_try_serialise_invalid_value(self):
        invalid_value = 'NotAnEc384PublicKey'

        with pytest.raises(TypeError, match='Value must be an ECDSA public key.'):
            Ec384PublicKey._try_serialise(invalid_value)
