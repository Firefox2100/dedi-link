import pytest
from deepdiff import DeepDiff
from copy import deepcopy

from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus, MessageType
from dedi_link.model import NetworkMessage
from dedi_link.model.network_message.network_auth_message import AuthRequestInvite


@pytest.fixture
def mock_auth_request_invite_1(mock_node_1):
    return AuthRequestInvite(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        auth_type=AuthMessageType.REQUEST,
        status=AuthMessageStatus.SENT,
        node=mock_node_1,
        target_url='https://node2.example.com',
        challenge=['accident', 'flip', 'royal'],
        justification='This is a test',
        message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_request_invite_dict_1(mock_node_dict_1):
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'authType': 'request',
            'targetUrl': 'https://node2.example.com',
            'status': 'sent',
        },
        'messageData': {
            'node': mock_node_dict_1,
            'challenge': ['accident', 'flip', 'royal'],
            'justification': 'This is a test',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_request_invite_2(mock_node_1, mock_network_1):
    return AuthRequestInvite(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        auth_type=AuthMessageType.INVITE,
        status=AuthMessageStatus.SENT,
        node=mock_node_1,
        target_url='https://node2.example.com',
        challenge=['pluck', 'humor', 'music'],
        justification='This is a test',
        message_id='6669a5d8-7802-42a1-99a4-a303c0a4253c',
        timestamp=1704067200,
        network=mock_network_1,
    )


@pytest.fixture
def mock_auth_request_invite_dict_2(mock_node_dict_1, mock_network_dict_1):
    network_dict = mock_network_dict_1.copy()
    network_dict.pop('nodeIds')
    network_dict.pop('instanceId')

    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '6669a5d8-7802-42a1-99a4-a303c0a4253c',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'authType': 'invite',
            'targetUrl': 'https://node2.example.com',
            'status': 'sent',
        },
        'messageData': {
            'node': mock_node_dict_1,
            'network': network_dict,
            'challenge': ['pluck', 'humor', 'music'],
            'justification': 'This is a test',
        },
        'timestamp': 1704067200,
    }


class TestAuthRequestInvite:
    def test_init(self, mock_node_1):
        auth_request_invite = AuthRequestInvite(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            auth_type=AuthMessageType.REQUEST,
            status=AuthMessageStatus.SENT,
            node=mock_node_1,
            target_url='https://node2.example.com',
            challenge=['accident', 'flip', 'royal'],
            justification='This is a test',
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            timestamp=1704067200,
        )

        assert auth_request_invite.message_type == MessageType.AUTH_MESSAGE
        assert auth_request_invite.auth_type == AuthMessageType.REQUEST
        assert auth_request_invite.status == AuthMessageStatus.SENT
        assert auth_request_invite.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_request_invite.node_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_request_invite.node == mock_node_1
        assert auth_request_invite.target_url == 'https://node2.example.com'
        assert auth_request_invite.challenge == ['accident', 'flip', 'royal']
        assert auth_request_invite.justification == 'This is a test'
        assert auth_request_invite.message_id == 'a63c273c-bad2-4521-a7ce-5c9a4c07682d'
        assert auth_request_invite.timestamp == 1704067200

    def test_init_invalid_auth_type(self, mock_node_1):
        with pytest.raises(ValueError):
            _ = AuthRequestInvite(
                network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                auth_type=AuthMessageType.JOIN,
                status=AuthMessageStatus.SENT,
                node=mock_node_1,
                target_url='https://node2.example.com',
                challenge=['accident', 'flip', 'royal'],
                justification='This is a test',
                message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
                timestamp=1704067200,
            )

    def test_init_generate_challenge(self, mock_node_1):
        auth_request_invite = AuthRequestInvite(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            auth_type=AuthMessageType.REQUEST,
            status=AuthMessageStatus.SENT,
            node=mock_node_1,
            target_url='https://node2.example.com',
            justification='This is a test',
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            timestamp=1704067200,
        )

        assert auth_request_invite.message_type == MessageType.AUTH_MESSAGE
        assert auth_request_invite.auth_type == AuthMessageType.REQUEST
        assert auth_request_invite.status == AuthMessageStatus.SENT
        assert auth_request_invite.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_request_invite.node_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_request_invite.node == mock_node_1
        assert auth_request_invite.target_url == 'https://node2.example.com'
        assert auth_request_invite.justification == 'This is a test'
        assert auth_request_invite.message_id == 'a63c273c-bad2-4521-a7ce-5c9a4c07682d'
        assert auth_request_invite.timestamp == 1704067200

        assert auth_request_invite.challenge is not None
        assert isinstance(auth_request_invite.challenge, list)
        assert len(auth_request_invite.challenge) == 3

        assert bool(DeepDiff(
            auth_request_invite.challenge,
            ['accident', 'flip', 'royal'],
            ignore_order=True,
        ))

    def test_init_network_mismatch(self, mock_node_1, mock_network_1):
        with pytest.raises(ValueError):
            _ = AuthRequestInvite(
                network_id='64b3b646-26eb-43c1-987d-3247b4a7e02a',
                node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                auth_type=AuthMessageType.INVITE,
                status=AuthMessageStatus.SENT,
                node=mock_node_1,
                target_url='https://node2.example.com',
                challenge=['pluck', 'humor', 'music'],
                justification='This is a test',
                message_id='6669a5d8-7802-42a1-99a4-a303c0a4253c',
                timestamp=1704067200,
                network=mock_network_1,
            )

    def test_equality(self,
                      mock_node_1,
                      mock_auth_request_invite_1,
                      mock_auth_request_invite_2,
                      ):
        assert mock_auth_request_invite_1 == AuthRequestInvite(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            auth_type=AuthMessageType.REQUEST,
            status=AuthMessageStatus.SENT,
            node=mock_node_1,
            target_url='https://node2.example.com',
            challenge=['accident', 'flip', 'royal'],
            justification='This is a test',
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            timestamp=1704067200,
        )

        assert mock_auth_request_invite_1 != mock_auth_request_invite_2

        assert mock_auth_request_invite_1 != 'Random String'

    def test_hash(self, mock_auth_request_invite_1):
        message_hash = hash(mock_auth_request_invite_1)

        assert isinstance(message_hash, int)

    def test_to_dict(self,
                     mock_auth_request_invite_1,
                     mock_auth_request_invite_2,
                     mock_auth_request_invite_dict_1,
                     mock_auth_request_invite_dict_2,
                     ):
        assert not DeepDiff(
            mock_auth_request_invite_1.to_dict(),
            mock_auth_request_invite_dict_1,
            ignore_order=True,
        )
        assert not DeepDiff(
            mock_auth_request_invite_2.to_dict(),
            mock_auth_request_invite_dict_2,
            ignore_order=True,
        )

    def test_from_dict(self,
                       mock_auth_request_invite_1,
                       mock_auth_request_invite_2,
                       mock_auth_request_invite_dict_1,
                       mock_auth_request_invite_dict_2,
                       ):
        auth_request_invite_1 = AuthRequestInvite.from_dict(mock_auth_request_invite_dict_1)
        auth_request_invite_2 = AuthRequestInvite.from_dict(mock_auth_request_invite_dict_2)

        assert auth_request_invite_1 == mock_auth_request_invite_1
        assert auth_request_invite_2 == mock_auth_request_invite_2

    def test_factory(self,
                     mock_auth_request_invite_1,
                     mock_auth_request_invite_2,
                     mock_auth_request_invite_dict_1,
                     mock_auth_request_invite_dict_2,
                     ):
        id_var_1 = MessageType(mock_auth_request_invite_dict_1['messageType'])
        id_var_2 = MessageType(mock_auth_request_invite_dict_2['messageType'])

        network_message_1 = NetworkMessage.factory(mock_auth_request_invite_dict_1, id_var_1)
        network_message_2 = NetworkMessage.factory(mock_auth_request_invite_dict_2, id_var_2)

        assert network_message_1 == mock_auth_request_invite_1
        assert network_message_2 == mock_auth_request_invite_2

    def test_generate_challenge(self, mock_auth_request_invite_1):
        auth_request_invite = deepcopy(mock_auth_request_invite_1)

        auth_request_invite.generate_challenge()

        assert auth_request_invite.challenge is not None
        assert isinstance(auth_request_invite.challenge, list)
        assert len(auth_request_invite.challenge) == 3

        assert bool(DeepDiff(
            auth_request_invite.challenge,
            ['accident', 'flip', 'royal'],
            ignore_order=True,
        ))
