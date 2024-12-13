import pytest
import json
import base64
from unittest.mock import patch, PropertyMock
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from dedi_link.etc.exceptions import NetworkMessageNotImplemented
from dedi_link.model import NetworkMessage, Network
from dedi_link.model.network_message import NetworkMessageHeader


class TestNetworkMessage:
    def test_init(self):
        network_message = NetworkMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='ef893ef0-1d29-4cae-ac61-0891f346fed3',
            timestamp=1704067200,
        )

        assert network_message.message_type is None
        assert network_message.message_id == 'ef893ef0-1d29-4cae-ac61-0891f346fed3'
        assert network_message.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert network_message.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_message.timestamp == 1704067200

    def test_equality(self,
                      mock_network_message_1,
                      mock_network_message_2,
                      ):
        assert mock_network_message_1 == NetworkMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='ef893ef0-1d29-4cae-ac61-0891f346fed3',
            timestamp=1704067200,
        )

        assert mock_network_message_1 != mock_network_message_2

        assert not mock_network_message_1 == 'Random String'

    def test_hash(self,
                  mock_network_message_1,
                  mock_network_message_2,
                  ):
        assert hash(mock_network_message_1) == hash(NetworkMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='ef893ef0-1d29-4cae-ac61-0891f346fed3',
            timestamp=1704067200,
        ))

        assert hash(mock_network_message_1) != hash(mock_network_message_2)

    def test_to_dict(self,
                     mock_network_message_1,
                     ):
        with pytest.raises(AttributeError):
            mock_network_message_1.to_dict()

    def test_from_dict(self):
        with pytest.raises(NetworkMessageNotImplemented):
            NetworkMessage.from_dict({})

    def test_signature(self,
                       mock_auth_join_1,
                       mock_public_key,
                       mock_private_key,
                       ):
        mock_network = Network(
            network_id='',
            network_name='',
        )

        with patch('dedi_link.model.network.Network.load', return_value=mock_network):
            with patch('dedi_link.model.network.Network.private_key', new_callable=PropertyMock) as mock_p_key:
                mock_p_key.return_value = mock_private_key

                signature = mock_auth_join_1.signature

                assert isinstance(signature, str)

                public_key = serialization.load_pem_public_key(
                    data=mock_public_key.encode(),
                )
                payload = json.dumps(mock_auth_join_1.to_dict())

                signature_bytes = base64.b64decode(signature.encode())

                public_key.verify(
                    signature_bytes,
                    payload.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256(),
                )

    def test_generate_headers(self, mock_network_message_1):
        with patch(
                'dedi_link.model.network_message.network_message.NetworkMessage.signature',
                new_callable=PropertyMock,
        ) as mock_signature:
            with patch(
                    'dedi_link.model.network_message.network_message.NetworkMessage.access_token',
                    new_callable=PropertyMock,
            ) as mock_access_token:
                mock_signature.return_value = 'signature'
                mock_access_token.return_value = 'access_token'

                headers = mock_network_message_1.generate_headers()

                assert headers == NetworkMessageHeader(
                    node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
                    network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                    server_signature='signature',
                    access_token='access_token',
                )
