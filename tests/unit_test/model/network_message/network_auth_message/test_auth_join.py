import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import AuthMessageType, MessageType
from dedi_link.model.network_message import NetworkMessage, NetworkAuthMessage
from dedi_link.model.network_message.network_auth_message import AuthJoin


@pytest.fixture
def mock_auth_join_1(mock_node_1):
    return AuthJoin(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        node=mock_node_1,
        message_id='1be8938b-f656-4c8b-9e45-93c84af95723',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_join_dict_1(mock_node_dict_1):
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '1be8938b-f656-4c8b-9e45-93c84af95723',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'join',
        },
        'messageData':{
            'node': mock_node_dict_1,
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_join_2(mock_node_2):
    return AuthJoin(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        node=mock_node_2,
        message_id='ddf9be31-319e-4592-8346-4cfd61a550fc',
        timestamp=1704067200,
    )


class TestAuthJoin:
    def test_init(self, mock_node_1):
        auth_join = AuthJoin(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            node=mock_node_1,
            message_id='1be8938b-f656-4c8b-9e45-93c84af95723',
            timestamp=1704067200,
        )

        assert auth_join.message_type == MessageType.AUTH_MESSAGE
        assert auth_join.auth_type == AuthMessageType.JOIN
        assert auth_join.message_id == '1be8938b-f656-4c8b-9e45-93c84af95723'
        assert auth_join.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_join.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert auth_join.node == mock_node_1
        assert auth_join.timestamp == 1704067200

    def test_equality(self,
                      mock_node_1,
                      mock_auth_join_1,
                      mock_auth_join_2,
                      ):
        assert mock_auth_join_1 == AuthJoin(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            node=mock_node_1,
            message_id='1be8938b-f656-4c8b-9e45-93c84af95723',
            timestamp=1704067200,
        )

        assert mock_auth_join_1 != mock_auth_join_2

        assert mock_auth_join_1 != 'Random String'

    def test_hash(self, mock_auth_join_1):
        message_hash = hash(mock_auth_join_1)

        assert isinstance(message_hash, int)

    def test_to_dict(self, mock_auth_join_1, mock_auth_join_dict_1):
        assert not DeepDiff(
            mock_auth_join_1.to_dict(),
            mock_auth_join_dict_1,
            ignore_order=True,
        )

    def test_from_dict(self, mock_auth_join_1, mock_auth_join_dict_1):
        auth_join = AuthJoin.from_dict(mock_auth_join_dict_1)

        assert auth_join == mock_auth_join_1

    def test_factory(self, mock_auth_join_1, mock_auth_join_dict_1):
        network_message = NetworkMessage.factory(mock_auth_join_dict_1)
        network_auth_message = NetworkAuthMessage.factory(mock_auth_join_dict_1)

        assert network_message == mock_auth_join_1
        assert network_auth_message == mock_auth_join_1
