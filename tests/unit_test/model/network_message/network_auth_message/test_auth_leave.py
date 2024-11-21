import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import AuthMessageType, MessageType
from dedi_link.model import NetworkMessage
from dedi_link.model.network_message.network_auth_message import AuthLeave


@pytest.fixture
def mock_auth_leave_1():
    return AuthLeave(
        network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
        node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        message_id='32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_leave_dict_1():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
            'networkId': '3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            'nodeId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'authType': 'leave',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_leave_2():
    return AuthLeave(
        network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
        node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        message_id='3edf7b0e-a811-43ee-b159-e75c22ed1d13',
        timestamp=1704067200,
    )


class TestAuthLeave:
    def test_init(self):
        auth_leave = AuthLeave(
            network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            message_id='32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
            timestamp=1704067200,
        )

        assert auth_leave.message_type == MessageType.AUTH_MESSAGE
        assert auth_leave.auth_type == AuthMessageType.LEAVE
        assert auth_leave.message_id == '32ee50ea-07e9-4667-9f0e-98b6fca8dfb4'
        assert auth_leave.network_id == '3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d'
        assert auth_leave.node_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_leave.timestamp == 1704067200

    def test_equality(self, mock_auth_leave_1, mock_auth_leave_2):
        assert mock_auth_leave_1 == AuthLeave(
            network_id='3ac1ed5a-0285-47f6-8b9c-12d16f3b3e2d',
            node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            message_id='32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
            timestamp=1704067200,
        )

        assert mock_auth_leave_1 != mock_auth_leave_2

        assert not mock_auth_leave_1 == 'Random String'

    def test_hash(self, mock_auth_leave_1):
        message_hash = hash(mock_auth_leave_1)

        assert isinstance(message_hash, int)

    def test_to_dict(self, mock_auth_leave_1, mock_auth_leave_dict_1):
        assert not DeepDiff(
            mock_auth_leave_1.to_dict(),
            mock_auth_leave_dict_1,
            ignore_order=True,
        )

    def test_from_dict(self, mock_auth_leave_1, mock_auth_leave_dict_1):
        auth_leave = AuthLeave.from_dict(mock_auth_leave_dict_1)

        assert auth_leave == mock_auth_leave_1

    def test_factory(self, mock_auth_leave_1, mock_auth_leave_dict_1):
        id_var = MessageType(mock_auth_leave_dict_1['messageType'])

        network_message = NetworkMessage.factory(mock_auth_leave_dict_1, id_var)
        assert network_message == mock_auth_leave_1
