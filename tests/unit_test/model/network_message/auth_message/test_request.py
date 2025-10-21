from pydantic import ValidationError
import pytest

from dedi_link.etc.enums import MessageType
from dedi_link.model.network_message.message_metadata import MessageMetadata
from dedi_link.model.network_message.auth_message.request import AuthRequest


class TestAuthRequest:
    def test_init(self,
                  network_id,
                  node_id,
                  sample_node,
                  ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42
        justification = 'Requesting to join the network for research purposes.'

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_request = AuthRequest(
            metadata=metadata,
            node=sample_node,
            challengeNonce=challenge_nonce,
            challengeSolution=challenge_solution,
            justification=justification,
        )

        assert auth_request.metadata.network_id == network_id
        assert auth_request.metadata.node_id == node_id
        assert auth_request.message_type == MessageType.AUTH_REQUEST
        assert auth_request.node == sample_node
        assert auth_request.challenge_nonce == challenge_nonce
        assert auth_request.challenge_solution == challenge_solution

    def test_model_validate(self,
                            network_id,
                            node_id,
                            sample_node,
                            ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42
        justification = 'Requesting to join the network for research purposes.'

        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_request_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_REQUEST,
            'node': sample_node.model_dump(),
            'challengeNonce': challenge_nonce,
            'challengeSolution': challenge_solution,
            'justification': justification,
        }

        auth_request = AuthRequest.model_validate(auth_request_dict)

        assert auth_request.metadata.network_id == network_id
        assert auth_request.metadata.node_id == node_id
        assert auth_request.message_type == MessageType.AUTH_REQUEST
        assert auth_request.node == sample_node
        assert auth_request.challenge_nonce == challenge_nonce
        assert auth_request.challenge_solution == challenge_solution

    def test_model_validate_invalid_message_type(self,
                                                 network_id,
                                                 node_id,
                                                 sample_node,
                                                 ):
            challenge_nonce = 'nonce123'
            challenge_solution = 42
            justification = 'Requesting to join the network for research purposes.'

            metadata_dict = {
                'networkId': str(network_id),
                'nodeId': str(node_id),
            }

            auth_request_dict = {
                'metadata': metadata_dict,
                'messageType': 'INVALID_TYPE',
                'node': sample_node.model_dump(),
                'challengeNonce': challenge_nonce,
                'challengeSolution': challenge_solution,
                'justification': justification,
            }

            with pytest.raises(ValidationError):
                AuthRequest.model_validate(auth_request_dict)

    def test_model_dump(self,
                        network_id,
                        node_id,
                        sample_node,
                        ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42
        justification = 'Requesting to join the network for research purposes.'

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_request = AuthRequest(
            metadata=metadata,
            node=sample_node,
            challengeNonce=challenge_nonce,
            challengeSolution=challenge_solution,
            justification=justification,
        )

        auth_request_dict = auth_request.model_dump(by_alias=True)

        assert auth_request_dict['metadata']['networkId'] == str(network_id)
        assert auth_request_dict['metadata']['nodeId'] == str(node_id)
        assert auth_request_dict['messageType'] == 'uk.co.firefox2100.ddg.auth.request'
        assert auth_request_dict['node'] == sample_node.model_dump(by_alias=True)
        assert auth_request_dict['challengeNonce'] == challenge_nonce
        assert auth_request_dict['challengeSolution'] == challenge_solution
        assert auth_request_dict['justification'] == justification

    def test_model_dump_json(self,
                             network_id,
                             node_id,
                             message_id,
                             timestamp,
                             sample_node,
                             ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42
        justification = 'Requesting to join the network for research purposes.'

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
            messageId=message_id,
            timestamp=timestamp,
        )

        auth_request = AuthRequest(
            metadata=metadata,
            node=sample_node,
            challengeNonce=challenge_nonce,
            challengeSolution=challenge_solution,
            justification=justification,
        )

        auth_request_json = auth_request.model_dump_json(by_alias=True)

        expected_json = f'''{{"metadata":{{"networkId":"{network_id}","nodeId":"{node_id}",\
"messageId":"{message_id}","timestamp":{timestamp}}},"messageType":"uk.co.firefox2100.ddg.auth.request",\
"node":{sample_node.model_dump_json(by_alias=True)},\
"challengeNonce":"{challenge_nonce}",\
"challengeSolution":{challenge_solution},\
"justification":"{justification}"}}'''

        assert auth_request_json == expected_json
