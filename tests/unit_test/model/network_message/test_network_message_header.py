import pytest
from deepdiff import DeepDiff

from dedi_link.model.network_message import NetworkMessageHeader


@pytest.fixture
def mock_network_message_header_1():
    return NetworkMessageHeader(
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
        server_signature='server_signature',
        access_token='access_token',
        user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
        delivered=True,
    )


@pytest.fixture
def mock_network_message_header_2():
    return NetworkMessageHeader(
        node_id='428fa5a2-132f-4a9e-981a-cad16ae702db',
        network_id='1560cbf8-29e4-4fee-af31-b88ebe61e440',
        server_signature='server_signature',
        access_token='access_token',
        user_id='9a05d3e5-7014-4416-ac2d-442cca395555',
        delivered=True,
    )


class TestNetworkMessageHeader:
    def test_init(self):
        network_message_header = NetworkMessageHeader(
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            server_signature='server_signature',
            access_token='access_token',
            user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            delivered=True,
        )

        assert network_message_header.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_message_header.network_id == '3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d'
        assert network_message_header.server_signature == 'server_signature'
        assert network_message_header.access_token == 'access_token'
        assert network_message_header.user_id == '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb'
        assert network_message_header.delivered is True

    def test_equality(self, mock_network_message_header_1, mock_network_message_header_2):
        assert mock_network_message_header_1 == NetworkMessageHeader(
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            server_signature='server_signature',
            access_token='access_token',
            user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            delivered=True,
        )

        assert mock_network_message_header_1 != mock_network_message_header_2

        assert not mock_network_message_header_1 == 'Random String'

    def test_hash(self, mock_network_message_header_1):
        message_hash = hash(mock_network_message_header_1)

        assert isinstance(message_hash, int)

    def test_headers(self, mock_network_message_header_1):
        payload = {
            'Content-Type': 'application/json',
            'X-Node-ID': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'X-Network-ID': '3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            'X-Server-Signature': 'server_signature',
            'Authorization': 'Bearer access_token',
            'X-User-ID': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            'X-Delivered': 'true',
        }

        assert not DeepDiff(
            mock_network_message_header_1.headers,
            payload,
            ignore_order=True,
        )

    def test_from_headers(self, mock_network_message_header_1):
        payload = {
            'Content-Type': 'application/json',
            'X-Node-ID': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'X-Network-ID': '3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            'X-Server-Signature': 'server_signature',
            'Authorization': 'Bearer access_token',
            'X-User-ID': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            'X-Delivered': 'true',
        }

        network_message_header = NetworkMessageHeader.from_headers(payload)

        assert network_message_header == mock_network_message_header_1
