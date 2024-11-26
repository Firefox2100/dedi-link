import pytest
from deepdiff import DeepDiff
from copy import deepcopy

from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus, MessageType
from dedi_link.model import NetworkMessage
from dedi_link.model.network_message.network_auth_message import AuthResponse


@pytest.fixture
def mock_auth_response_1(mock_node_2, mock_network_1):
    return AuthResponse(
        message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
        approved=True,
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
        node=mock_node_2,
        timestamp=1704067200,
        network=mock_network_1,
    )


@pytest.fixture
def mock_auth_response_dict_1(mock_node_dict_2, mock_network_dict_1):
    network_dict = mock_network_dict_1.copy()
    network_dict.pop('nodeIds')
    network_dict.pop('instanceId')

    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'd3398f33-e621-465c-846f-f7f79dff6a87',
            'authType': 'response',
            'approved': True,
        },
        'messageData': {
            'node': mock_node_dict_2,
            'network': network_dict,
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_response_2():
    return AuthResponse(
        message_id='6669a5d8-7802-42a1-99a4-a303c0a4253c',
        approved=False,
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_response_dict_2():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '6669a5d8-7802-42a1-99a4-a303c0a4253c',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'd3398f33-e621-465c-846f-f7f79dff6a87',
            'authType': 'response',
            'approved': False,
        },
        'timestamp': 1704067200,
    }


class TestAuthResponse:
    def test_init(self, mock_node_2, mock_network_1):
        auth_response = AuthResponse(
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            approved=True,
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
            node=mock_node_2,
            timestamp=1704067200,
            network=mock_network_1,
        )

        assert auth_response.message_id == 'a63c273c-bad2-4521-a7ce-5c9a4c07682d'
        assert auth_response.approved == True
        assert auth_response.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_response.node_id == 'd3398f33-e621-465c-846f-f7f79dff6a87'
        assert auth_response.node == mock_node_2
        assert auth_response.timestamp == 1704067200
        assert auth_response.network == mock_network_1
        assert auth_response.auth_type == AuthMessageType.RESPONSE
        assert auth_response.message_type == MessageType.AUTH_MESSAGE

    def test_init_missing_node(self, mock_network_1):
        with pytest.raises(ValueError):
            _ = AuthResponse(
                message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
                approved=True,
                network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
                timestamp=1704067200,
                network=mock_network_1,
            )

    def test_init_node_id_mismatch(self, mock_node_2, mock_network_1):
        with pytest.raises(ValueError):
            _ = AuthResponse(
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            approved=True,
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='1c2a77f6-f5fe-4750-861c-c8cde5e66e74',
            node=mock_node_2,
            timestamp=1704067200,
            network=mock_network_1,
        )

    def test_init_network_id_mismatch(self, mock_node_2, mock_network_1):
        with pytest.raises(ValueError):
            _ = AuthResponse(
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            approved=True,
            network_id='e6405c8e-6d78-4a9f-abc4-db23af1e771c',
            node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
            node=mock_node_2,
            timestamp=1704067200,
            network=mock_network_1,
        )

    def test_equality(self,
                      mock_node_2,
                      mock_network_1,
                      mock_auth_response_1,
                      mock_auth_response_2,
                      ):
        assert mock_auth_response_1 == AuthResponse(
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            approved=True,
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
            node=mock_node_2,
            timestamp=1704067200,
            network=mock_network_1,
        )

        assert mock_auth_response_1 != mock_auth_response_2

        assert mock_auth_response_1 != 'Random String'

    def test_hash(self, mock_auth_response_1):
        message_hash = hash(mock_auth_response_1)

        assert isinstance(message_hash, int)

    def test_to_dict(self,
                     mock_auth_response_1,
                     mock_auth_response_2,
                     mock_auth_response_dict_1,
                     mock_auth_response_dict_2,
                     ):
        assert not DeepDiff(
            mock_auth_response_1.to_dict(),
            mock_auth_response_dict_1,
            ignore_order=True,
        )
        assert not DeepDiff(
            mock_auth_response_2.to_dict(),
            mock_auth_response_dict_2,
            ignore_order=True,
        )

    def test_from_dict(self,
                       mock_auth_response_1,
                       mock_auth_response_2,
                       mock_auth_response_dict_1,
                       mock_auth_response_dict_2,
                       ):
        assert mock_auth_response_1 == AuthResponse.from_dict(mock_auth_response_dict_1)
        assert mock_auth_response_2 == AuthResponse.from_dict(mock_auth_response_dict_2)
