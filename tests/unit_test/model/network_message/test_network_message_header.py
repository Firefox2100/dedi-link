import pytest
from deepdiff import DeepDiff

from dedi_link.model.network_message import NetworkMessageHeader


class TestNetworkMessageHeader:
    def test_init(self):
        network_message_header = NetworkMessageHeader(
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            server_signature='server_signature',
            access_token='access_token',
            user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            delivered=True,
        )

        assert network_message_header.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_message_header.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert network_message_header.server_signature == 'server_signature'
        assert network_message_header.access_token == 'access_token'
        assert network_message_header.user_id == '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb'
        assert network_message_header.delivered is True

    def test_equality(self, mock_network_message_header_1, mock_network_message_header_2):
        assert mock_network_message_header_1 == NetworkMessageHeader(
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
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

    def test_headers(self,
                     mock_network_message_header_1,
                     mock_network_message_header_dict_1,
                     ):
        assert not DeepDiff(
            mock_network_message_header_1.headers,
            mock_network_message_header_dict_1,
            ignore_order=True,
        )

    def test_from_headers(self,
                          mock_network_message_header_1,
                          mock_network_message_header_dict_1,
                          ):
        network_message_header = NetworkMessageHeader.from_headers(mock_network_message_header_dict_1)

        assert network_message_header == mock_network_message_header_1
