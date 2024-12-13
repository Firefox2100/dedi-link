import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import AuthMessageType, MessageType
from dedi_link.model.network_message import NetworkAuthMessage


@pytest.fixture
def mock_network_auth_message_1():
    return NetworkAuthMessage(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        message_id='3d1b4f89-7f80-4aea-b57d-8c797cdf9e70',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_network_auth_message_2():
    return NetworkAuthMessage(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        message_id='48fda6b6-ae98-4956-be83-78103429025e',
        timestamp=1704067200,
    )


class TestNetworkAuthMessage:
    def test_init(self):
        network_auth_message = NetworkAuthMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='3d1b4f89-7f80-4aea-b57d-8c797cdf9e70',
            timestamp=1704067200,
        )

        assert network_auth_message.message_type == MessageType.AUTH_MESSAGE
        assert network_auth_message.message_id == '3d1b4f89-7f80-4aea-b57d-8c797cdf9e70'
        assert network_auth_message.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert network_auth_message.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_auth_message.auth_type is None
        assert network_auth_message.timestamp == 1704067200

    def test_equality(self, mock_network_auth_message_1, mock_network_auth_message_2):
        assert mock_network_auth_message_1 == NetworkAuthMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='3d1b4f89-7f80-4aea-b57d-8c797cdf9e70',
            timestamp=1704067200,
        )

        assert mock_network_auth_message_1 != mock_network_auth_message_2

        assert not mock_network_auth_message_1 == 'Random String'

    def test_hash(self, mock_network_auth_message_1):
        message_hash = hash(mock_network_auth_message_1)

        assert isinstance(message_hash, int)

    def test_to_dict(self, mock_network_auth_message_1):
        with pytest.raises(AttributeError):
            # The auth_type defaults to None, so cannot call it on base class
            mock_network_auth_message_1.to_dict()
