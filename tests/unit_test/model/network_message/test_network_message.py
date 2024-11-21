import pytest
import json
import base64
from unittest.mock import patch, PropertyMock
from deepdiff import DeepDiff
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import NetworkMessageNotImplemented
from dedi_link.model import NetworkMessage, Network
from dedi_link.model.network_message import NetworkMessageHeader


@pytest.fixture
def mock_network_message_1():
    return NetworkMessage(
        message_type=MessageType.AUTH_MESSAGE,
        network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        message_id='ef893ef0-1d29-4cae-ac61-0891f346fed3',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_network_message_2():
    return NetworkMessage(
        message_type=MessageType.AUTH_MESSAGE,
        network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        message_id='41b0a563-d0fe-46f4-ae43-813a36914a65',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_public_key():
    return """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAjdXv5L1sjDnfK43Cwasd
q2cRDl3tJKbOJ97G2PdyCH0m27Ra28vsmijeMJnUZPYfatjoXgWPRbpR8cUwef/o
RcSbUAskvp+hcMEp6sTAP6IFcOLrltzMgjV2wT4WqP3Tkb6AZyvXDvGJSs0GdAl9
WL9SGOzk80BJNiAwDedPMwtxQWbk5nmP1RK9azgF6CQqaYohvv7jhNlZUElYW9eA
zQ/0I1RYDaIa5M6G/Z5ak32+3UM6f4wYqzA3nnpl6zPCi1Siuu57iNEM/EYel8uv
2skTCkl7zViQFr1Z9blAodhrMpaV3oyum9jczUcQ5gkTMn8VvQsrdCFvZbfPak7B
xrP/hDC9HWwit4DkpKjEpOszM99AxC6O/IEFLx0y09lFgv7V/OQQ3FKsjwimGnIe
XmQ9XRGvjMxuVjRW8gOeR6ypNegrcMoLmXiV3DLXnLonOiLyszTXs/xnmkFS7WHO
12K5PE7qIQZxf7kh6iR34HAng7MA0nOGPT3SkcE8VsC8A3Gs1by2mikKqsUN+Im4
OZm0AIYOz2/ytz7ArHkkfiwxzSSJ9f5YURsxFH0UH0mbbuDsMXOf+95t9s1uBSjX
pUzc/Rt0G8YErT1OkmvVG9y2xlhj/Mr1SujBab4jKMyM2sc3NMWsBqWkYT/YcWRf
j65o4mLG79hyNTpsfmRa5gECAwEAAQ==
-----END PUBLIC KEY-----
"""


@pytest.fixture
def mock_private_key():
    return """
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""


class TestNetworkMessage:
    def test_init(self):
        network_message = NetworkMessage(
            message_type=MessageType.AUTH_MESSAGE,
            network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='ef893ef0-1d29-4cae-ac61-0891f346fed3',
            timestamp=1704067200,
        )

        assert network_message.message_type == MessageType.AUTH_MESSAGE
        assert network_message.message_id == 'ef893ef0-1d29-4cae-ac61-0891f346fed3'
        assert network_message.network_id == '3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d'
        assert network_message.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_message.timestamp == 1704067200

    def test_equality(self, mock_network_message_1, mock_network_message_2):
        assert mock_network_message_1 == NetworkMessage(
            message_type=MessageType.AUTH_MESSAGE,
            network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='ef893ef0-1d29-4cae-ac61-0891f346fed3',
            timestamp=1704067200,
        )

        assert mock_network_message_1 != mock_network_message_2

        assert not mock_network_message_1 == 'Random String'

    def test_hash(self, mock_network_message_1):
        message_hash = hash(mock_network_message_1)

        assert isinstance(message_hash, int)

    def test_to_dict(self, mock_network_message_1):
        payload = {
            'messageType': 'authMessage',
            'messageAttributes': {
                'messageId': 'ef893ef0-1d29-4cae-ac61-0891f346fed3',
                'networkId': '3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
                'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            },
            'timestamp': 1704067200,
        }

        assert not DeepDiff(
            mock_network_message_1.to_dict(),
            payload,
            ignore_order=True,
        )

    def test_from_dict(self):
        with pytest.raises(NetworkMessageNotImplemented):
            NetworkMessage.from_dict({})

    def test_signature(self, mock_network_message_1, mock_public_key, mock_private_key):
        mock_network = Network(
            network_id='',
            network_name='',
        )

        with patch('dedi_link.model.network.Network.load', return_value=mock_network):
            with patch('dedi_link.model.network.Network.private_key', new_callable=PropertyMock) as mock_p_key:
                mock_p_key.return_value = mock_private_key

                signature = mock_network_message_1.signature

                assert isinstance(signature, str)

                public_key = serialization.load_pem_public_key(
                    data=mock_public_key.encode(),
                )
                payload = json.dumps(mock_network_message_1.to_dict())

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
                    network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
                    server_signature='signature',
                    access_token='access_token',
                )
