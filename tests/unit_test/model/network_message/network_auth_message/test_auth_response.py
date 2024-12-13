import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import AuthMessageType, MessageType
from dedi_link.model.network_message import NetworkMessage, NetworkAuthMessage
from dedi_link.model.network_message.network_auth_message import AuthResponse

from unit_test.consts import NETWORK_IDS, NODE_IDS


class TestAuthResponse:
    def test_init(self, mock_node_1, mock_network_1):
        auth_response = AuthResponse(
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            approved=True,
            network_id=NETWORK_IDS[0],
            node_id=NODE_IDS[1],
            node=mock_node_1,
            timestamp=1704067200,
            network=mock_network_1,
        )

        assert auth_response.message_id == 'a63c273c-bad2-4521-a7ce-5c9a4c07682d'
        assert auth_response.approved == True
        assert auth_response.network_id == NETWORK_IDS[0]
        assert auth_response.node_id == NODE_IDS[1]
        assert auth_response.node == mock_node_1
        assert auth_response.timestamp == 1704067200
        assert auth_response.network == mock_network_1
        assert auth_response.auth_type == AuthMessageType.RESPONSE
        assert auth_response.message_type == MessageType.AUTH_MESSAGE

    def test_init_missing_node(self, mock_network_1):
        with pytest.raises(ValueError):
            _ = AuthResponse(
                message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
                approved=True,
                network_id=NETWORK_IDS[0],
                node_id=NODE_IDS[1],
                timestamp=1704067200,
                network=mock_network_1,
            )

    def test_init_node_id_mismatch(self, mock_node_2, mock_network_1):
        with pytest.raises(ValueError):
            _ = AuthResponse(
                message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
                approved=True,
                network_id=NETWORK_IDS[0],
                node_id=NODE_IDS[1],
                node=mock_node_2,
                timestamp=1704067200,
                network=mock_network_1,
            )

    def test_init_network_id_mismatch(self, mock_node_1, mock_network_1):
        with pytest.raises(ValueError):
            _ = AuthResponse(
                message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
                approved=True,
                network_id=NETWORK_IDS[1],
                node_id=NODE_IDS[1],
                node=mock_node_1,
                timestamp=1704067200,
                network=mock_network_1,
            )

    def test_equality(self,
                      mock_node_1,
                      mock_network_1,
                      mock_auth_response_1,
                      mock_auth_response_2,
                      ):
        assert mock_auth_response_1 == AuthResponse(
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            approved=True,
            network_id=NETWORK_IDS[0],
            node_id=NODE_IDS[1],
            node=mock_node_1,
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

    def test_factory(self,
                     mock_auth_response_1,
                     mock_auth_response_dict_1,
                     ):
        network_message = NetworkMessage.factory(mock_auth_response_dict_1)
        network_auth_message = NetworkAuthMessage.factory(mock_auth_response_dict_1)

        assert network_message == mock_auth_response_1
        assert network_auth_message == mock_auth_response_1
