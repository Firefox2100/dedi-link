from deepdiff import DeepDiff

from dedi_link.etc.enums import AuthMessageType, MessageType
from dedi_link.model.network_message import NetworkMessage, NetworkAuthMessage
from dedi_link.model.network_message.network_auth_message import AuthLeave


class TestAuthLeave:
    def test_init(self):
        auth_leave = AuthLeave(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            message_id='32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
            timestamp=1704067200,
        )

        assert auth_leave.message_type == MessageType.AUTH_MESSAGE
        assert auth_leave.auth_type == AuthMessageType.LEAVE
        assert auth_leave.message_id == '32ee50ea-07e9-4667-9f0e-98b6fca8dfb4'
        assert auth_leave.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_leave.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert auth_leave.timestamp == 1704067200

    def test_equality(self, mock_auth_leave_1, mock_auth_leave_2):
        assert mock_auth_leave_1 == AuthLeave(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
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
        network_message = NetworkMessage.factory(mock_auth_leave_dict_1)
        network_auth_message = NetworkAuthMessage.factory(mock_auth_leave_dict_1)

        assert network_message == mock_auth_leave_1
        assert network_auth_message == mock_auth_leave_1
