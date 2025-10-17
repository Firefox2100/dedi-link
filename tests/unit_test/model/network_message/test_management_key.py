from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from pydantic import ValidationError
import pytest

from dedi_link.model.network_message.management_key import NetworkManagementKey
from dedi_link.model.crypto_key import Ec384PublicKey, Ec384PrivateKey


class TestNetworkManagementKey:
    def test_init(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()

        management_key = NetworkManagementKey(
            publicKey=Ec384PublicKey(public_key),
            privateKey=Ec384PrivateKey(private_key)
        )

        assert management_key.public_key.public_key.public_numbers() == public_key.public_numbers()
        assert management_key.private_key.private_key.private_numbers() == private_key.private_numbers()

        management_key = NetworkManagementKey(
            publicKey=Ec384PublicKey(public_key),
        )

        assert management_key.public_key.public_key.public_numbers() == public_key.public_numbers()
        assert management_key.private_key is None

    def test_model_validate(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        management_key_dict = {
            'publicKey': pem_public_key,
            'privateKey': pem_private_key
        }

        management_key = NetworkManagementKey.model_validate(management_key_dict)

        assert management_key.public_key.public_key.public_numbers() == public_key.public_numbers()
        assert management_key.private_key.private_key.private_numbers() == private_key.private_numbers()

    def test_model_validate_invalid_public_key(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        management_key_dict = {
            'publicKey': 'InvalidPublicKey',
            'privateKey': pem_private_key
        }

        with pytest.raises(ValidationError):
            NetworkManagementKey.model_validate(management_key_dict)

    def test_model_validate_invalid_private_key(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        management_key_dict = {
            'publicKey': pem_public_key,
            'privateKey': 'InvalidPrivateKey'
        }

        with pytest.raises(ValidationError):
            NetworkManagementKey.model_validate(management_key_dict)

    def test_model_validate_private_key_none(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        management_key_dict = {
            'publicKey': pem_public_key,
            'privateKey': None
        }

        management_key = NetworkManagementKey.model_validate(management_key_dict)

        assert management_key.public_key.public_key.public_numbers() == public_key.public_numbers()
        assert management_key.private_key is None

    def test_model_dump(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        management_key = NetworkManagementKey(
            publicKey=Ec384PublicKey(public_key),
            privateKey=Ec384PrivateKey(private_key)
        )

        management_key_dict = management_key.model_dump()
        assert management_key_dict == {
            'publicKey': pem_public_key,
            'privateKey': pem_private_key
        }

        management_key = NetworkManagementKey(
            publicKey=Ec384PublicKey(public_key),
        )

        management_key_dict = management_key.model_dump()
        assert management_key_dict == {
            'publicKey': pem_public_key,
            'privateKey': None
        }

    def test_model_dump_json(self):
        private_key = ec.generate_private_key(
            curve=ec.SECP384R1(),
        )
        public_key = private_key.public_key()
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode().replace('\n', '\\n')
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode().replace('\n', '\\n')

        management_key = NetworkManagementKey(
            publicKey=Ec384PublicKey(public_key),
            privateKey=Ec384PrivateKey(private_key)
        )

        management_key_json = management_key.model_dump_json()
        expected_json = f'{{"publicKey":"{pem_public_key}","privateKey":"{pem_private_key}"}}'
        assert management_key_json == expected_json

        management_key = NetworkManagementKey(
            publicKey=Ec384PublicKey(public_key),
        )

        management_key_json = management_key.model_dump_json()
        expected_json = f'{{"publicKey":"{pem_public_key}","privateKey":null}}'
        assert management_key_json == expected_json
