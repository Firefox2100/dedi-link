import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import AuthMessageType, MessageType, AuthMessageStatus
from dedi_link.model.network_message import NetworkMessage, NetworkAuthMessage
from dedi_link.model.network_message.network_auth_message import AuthStatus


@pytest.fixture
def mock_auth_status_1():
    return AuthStatus(
        message_id='fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_dict_1():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'status',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_status_2():
    return AuthStatus(
        message_id='b75c30a2-f7bd-46a3-87eb-bf871c48e0e9',
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        status=AuthMessageStatus.ACCEPTED,
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_dict_2():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'b75c30a2-f7bd-46a3-87eb-bf871c48e0e9',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'status',
            'status': 'accepted',
        },
        'timestamp': 1704067200,
    }


class TestAuthStatus:
    def test_init(self):
        auth_status = AuthStatus(
            message_id='fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            timestamp=1704067200,
        )

        assert auth_status.message_type == MessageType.AUTH_MESSAGE
        assert auth_status.auth_type == AuthMessageType.STATUS
        assert auth_status.message_id == 'fbdd4729-2a0d-4f99-8b6c-3ce08bafa091'
        assert auth_status.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_status.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert auth_status.timestamp == 1704067200
        assert auth_status.status is None

    def test_equality(self,
                      mock_auth_status_1,
                      mock_auth_status_2,
                      ):
        assert mock_auth_status_1 == AuthStatus(
            message_id='fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            timestamp=1704067200,
        )

        assert mock_auth_status_1 != mock_auth_status_2

        assert mock_auth_status_1 != 'Random String'

    def test_hash(self, mock_auth_status_1):
        assert isinstance(hash(mock_auth_status_1), int)

    def test_to_dict(self,
                     mock_auth_status_1,
                     mock_auth_status_2,
                     mock_auth_status_dict_1,
                     mock_auth_status_dict_2,
                     ):
        assert not DeepDiff(
            mock_auth_status_1.to_dict(),
            mock_auth_status_dict_1,
            ignore_order=True,
        )
        assert not DeepDiff(
            mock_auth_status_2.to_dict(),
            mock_auth_status_dict_2,
            ignore_order=True,
        )

    def test_from_dict(self,
                       mock_auth_status_1,
                       mock_auth_status_2,
                       mock_auth_status_dict_1,
                       mock_auth_status_dict_2,
                       ):
        auth_status_1 = AuthStatus.from_dict(mock_auth_status_dict_1)
        auth_status_2 = AuthStatus.from_dict(mock_auth_status_dict_2)

        assert auth_status_1 == mock_auth_status_1
        assert auth_status_2 == mock_auth_status_2

    def test_factory(self,
                     mock_auth_status_1,
                     mock_auth_status_dict_1,
                     ):
        network_message = NetworkMessage.factory(mock_auth_status_dict_1)
        network_auth_message = NetworkAuthMessage.factory(mock_auth_status_dict_1)

        assert network_message == mock_auth_status_1
        assert network_auth_message == mock_auth_status_1
