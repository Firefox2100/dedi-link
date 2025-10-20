from uuid import uuid4, UUID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from pydantic import ValidationError
import pytest

from dedi_link.model.node import Node
from dedi_link.model.crypto_key import Ec384PublicKey


class TestNode:
    def test_init(self,
                  node_id,
                  ecdsa_p384_key_pair,
                  public_key,
                  ):
        _, p_key = ecdsa_p384_key_pair

        node = Node(
            nodeId=node_id,
            nodeName='Test Node',
            url='https://testnode.example.com/api/.well-known/discovery-gateway',
            description='A test node for unit testing.',
            publicKey=public_key,
            approved=True,
        )

        assert node.node_id == node_id
        assert node.node_name == 'Test Node'
        assert node.url == 'https://testnode.example.com/api/.well-known/discovery-gateway'
        assert node.description == 'A test node for unit testing.'
        assert node.public_key.public_key.public_numbers() == p_key.public_numbers()
        assert node.approved is True

        node = Node(
            nodeName='Test Node',
            url='https://testnode.example.com/api/.well-known/discovery-gateway',
            description='A test node for unit testing.',
        )

        assert isinstance(node.node_id, UUID)
        assert node.public_key is None
        assert node.approved is False

    def test_model_validate(self,
                            node_id,
                            ecdsa_p384_key_pair,
                            ):
        _, p_key = ecdsa_p384_key_pair
        pem_public_key = p_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        node_dict = {
            'nodeId': str(node_id),
            'nodeName': 'Test Node',
            'url': 'https://testnode.example.com/api/.well-known/discovery-gateway',
            'description': 'A test node for unit testing.',
            'publicKey': pem_public_key,
            'approved': True,
        }

        node = Node.model_validate(node_dict)

        assert node.node_id == node_id
        assert node.node_name == 'Test Node'
        assert node.url == 'https://testnode.example.com/api/.well-known/discovery-gateway'
        assert node.description == 'A test node for unit testing.'
        assert node.public_key.public_key.public_numbers() == p_key.public_numbers()
        assert node.approved is True

        # Test invalid public key
        node_dict['publicKey'] = 'invalid-key'
        with pytest.raises(ValidationError) as exc_info:
            Node.model_validate(node_dict)
        assert 'Invalid public key format.' in str(exc_info.value)

    def test_model_dump(self,
                        node_id,
                        ecdsa_p384_key_pair,
                        public_key,
                        ):
        _, p_key = ecdsa_p384_key_pair
        pem_public_key = p_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        node = Node(
            nodeId=node_id,
            nodeName='Test Node',
            url='https://testnode.example.com/api/.well-known/discovery-gateway',
            description='A test node for unit testing.',
            publicKey=public_key,
            approved=True,
        )

        node_dict = node.model_dump()
        assert node_dict == {
            'nodeId': str(node_id),
            'nodeName': 'Test Node',
            'url': 'https://testnode.example.com/api/.well-known/discovery-gateway',
            'description': 'A test node for unit testing.',
            'publicKey': pem_public_key,
            'approved': True,
        }

    def test_model_dump_json(self,
                             node_id,
                             ecdsa_p384_key_pair,
                             public_key,
                             ):
        _, p_key = ecdsa_p384_key_pair
        pem_public_key = p_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode().replace('\n', '\\n')

        node = Node(
            nodeId=node_id,
            nodeName='Test Node',
            url='https://testnode.example.com/api/.well-known/discovery-gateway',
            description='A test node for unit testing.',
            publicKey=public_key,
            approved=True,
        )

        node_json = node.model_dump_json()
        expected_json = (
            f'{{"nodeId":"{str(node_id)}",'
            f'"nodeName":"Test Node",'
            f'"url":"https://testnode.example.com/api/.well-known/discovery-gateway",'
            f'"description":"A test node for unit testing.",'
            f'"publicKey":"{pem_public_key}",'
            f'"approved":true}}'
        )
        assert node_json == expected_json
