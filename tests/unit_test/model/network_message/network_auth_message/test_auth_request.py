import pytest
from deepdiff import DeepDiff
from copy import deepcopy

from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus, MessageType
from dedi_link.model.network_message import NetworkMessage, NetworkAuthMessage
from dedi_link.model.network_message.network_auth_message import AuthRequest


class TestAuthRequest:
    def test_init(self, mock_node_1):
        auth_request = AuthRequest(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            status=AuthMessageStatus.SENT,
            node=mock_node_1,
            target_url='https://node2.example.com',
            challenge=['accident', 'flip', 'royal'],
            justification='This is a test',
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            timestamp=1704067200,
        )

        assert auth_request.message_type == MessageType.AUTH_MESSAGE
        assert auth_request.auth_type == AuthMessageType.REQUEST
        assert auth_request.status == AuthMessageStatus.SENT
        assert auth_request.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_request.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert auth_request.node == mock_node_1
        assert auth_request.target_url == 'https://node2.example.com'
        assert auth_request.challenge == ['accident', 'flip', 'royal']
        assert auth_request.justification == 'This is a test'
        assert auth_request.message_id == 'a63c273c-bad2-4521-a7ce-5c9a4c07682d'
        assert auth_request.timestamp == 1704067200

    def test_init_generate_challenge(self, mock_node_1):
        auth_request = AuthRequest(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            status=AuthMessageStatus.SENT,
            node=mock_node_1,
            target_url='https://node2.example.com',
            justification='This is a test',
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            timestamp=1704067200,
        )

        assert auth_request.message_type == MessageType.AUTH_MESSAGE
        assert auth_request.auth_type == AuthMessageType.REQUEST
        assert auth_request.status == AuthMessageStatus.SENT
        assert auth_request.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert auth_request.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert auth_request.node == mock_node_1
        assert auth_request.target_url == 'https://node2.example.com'
        assert auth_request.justification == 'This is a test'
        assert auth_request.message_id == 'a63c273c-bad2-4521-a7ce-5c9a4c07682d'
        assert auth_request.timestamp == 1704067200

        assert auth_request.challenge is not None
        assert isinstance(auth_request.challenge, list)
        assert len(auth_request.challenge) == 3

        assert bool(DeepDiff(
            auth_request.challenge,
            ['accident', 'flip', 'royal'],
            ignore_order=True,
        ))

    def test_equality(self,
                      mock_node_1,
                      mock_auth_request_1,
                      mock_auth_request_2,
                      ):
        assert mock_auth_request_1 == AuthRequest(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            status=AuthMessageStatus.SENT,
            node=mock_node_1,
            target_url='https://node2.example.com',
            challenge=['accident', 'flip', 'royal'],
            justification='This is a test',
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            timestamp=1704067200,
        )

        assert mock_auth_request_1 != mock_auth_request_2

        assert mock_auth_request_1 != 'Random String'

    def test_hash(self,
                  mock_node_1,
                  mock_auth_request_1,
                  mock_auth_request_2,):
        assert hash(mock_auth_request_1) == hash(AuthRequest(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            status=AuthMessageStatus.SENT,
            node=mock_node_1,
            target_url='https://node2.example.com',
            challenge=['accident', 'flip', 'royal'],
            justification='This is a test',
            message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            timestamp=1704067200,
        ))

        assert hash(mock_auth_request_1) != hash(mock_auth_request_2)

    def test_to_dict(self,
                     mock_auth_request_1,
                     mock_auth_request_2,
                     mock_auth_request_dict_1,
                     mock_auth_request_dict_2,
                     ):
        assert not DeepDiff(
            mock_auth_request_1.to_dict(),
            mock_auth_request_dict_1,
            ignore_order=True,
        )
        assert not DeepDiff(
            mock_auth_request_2.to_dict(),
            mock_auth_request_dict_2,
            ignore_order=True,
        )

    def test_from_dict(self,
                       mock_auth_request_1,
                       mock_auth_request_2,
                       mock_auth_request_dict_1,
                       mock_auth_request_dict_2,
                       ):
        auth_request_1 = AuthRequest.from_dict(mock_auth_request_dict_1)
        auth_request_2 = AuthRequest.from_dict(mock_auth_request_dict_2)

        assert auth_request_1 == mock_auth_request_1
        assert auth_request_2 == mock_auth_request_2

    def test_factory(self,
                     mock_auth_request_1,
                     mock_auth_request_2,
                     mock_auth_request_dict_1,
                     mock_auth_request_dict_2,
                     ):
        network_message_1 = NetworkMessage.factory(mock_auth_request_dict_1)
        network_message_2 = NetworkMessage.factory(mock_auth_request_dict_2)

        network_auth_message_1 = NetworkAuthMessage.factory(mock_auth_request_dict_1)
        network_auth_message_2 = NetworkAuthMessage.factory(mock_auth_request_dict_2)

        assert network_message_1 == mock_auth_request_1
        assert network_message_2 == mock_auth_request_2
        assert network_auth_message_1 == mock_auth_request_1
        assert network_auth_message_2 == mock_auth_request_2

    def test_generate_challenge(self, mock_auth_request_1):
        auth_request = deepcopy(mock_auth_request_1)

        auth_request.generate_challenge()

        assert auth_request.challenge is not None
        assert isinstance(auth_request.challenge, list)
        assert len(auth_request.challenge) == 3

        assert bool(DeepDiff(
            auth_request.challenge,
            ['accident', 'flip', 'royal'],
            ignore_order=True,
        ))
