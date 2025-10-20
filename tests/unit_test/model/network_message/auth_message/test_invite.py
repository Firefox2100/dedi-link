from uuid import uuid4
from pydantic import ValidationError
import pytest

from dedi_link.etc.enums import MessageType
from dedi_link.model.network_message.message_metadata import MessageMetadata
from dedi_link.model.network_message.auth_message.invite import AuthInvite


class TestAuthInvite:
    def test_init(self,
                  network_id,
                  node_id,
                  sample_network,
                  sample_node,
                  sample_management_key,
                  ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_invite = AuthInvite(
            metadata=metadata,
            network=sample_network,
            node=sample_node,
            managementKey=sample_management_key,
            challengeNonce=challenge_nonce,
            challengeSolution=challenge_solution,
        )

        assert auth_invite.metadata.network_id == network_id
        assert auth_invite.metadata.node_id == node_id
        assert auth_invite.message_type == MessageType.AUTH_INVITE
        assert auth_invite.network == sample_network
        assert auth_invite.node == sample_node
        assert auth_invite.management_key == sample_management_key
        assert auth_invite.challenge_nonce == challenge_nonce
        assert auth_invite.challenge_solution == challenge_solution

    def test_model_validate(self,
                            network_id,
                            node_id,
                            sample_network,
                            sample_node,
                            sample_management_key,
                            ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42

        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_invite_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_INVITE,
            'network': sample_network.model_dump(by_alias=True),
            'node': sample_node.model_dump(by_alias=True),
            'managementKey': sample_management_key.model_dump(by_alias=True),
            'challengeNonce': challenge_nonce,
            'challengeSolution': challenge_solution,
        }

        auth_invite = AuthInvite.model_validate(auth_invite_dict)

        assert auth_invite.metadata.network_id == network_id
        assert auth_invite.metadata.node_id == node_id
        assert auth_invite.message_type == MessageType.AUTH_INVITE
        assert auth_invite.network == sample_network
        assert auth_invite.node == sample_node
        assert auth_invite.management_key == sample_management_key
        assert auth_invite.challenge_nonce == challenge_nonce
        assert auth_invite.challenge_solution == challenge_solution

    def test_model_validate_invalid_message_type(self,
                                                 network_id,
                                                 node_id,
                                                 sample_network,
                                                 sample_node,
                                                 sample_management_key,
                                                 ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42

        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_invite_dict = {
            'metadata': metadata_dict,
            'messageType': 'INVALID_TYPE',
            'network': sample_network.model_dump(by_alias=True),
            'node': sample_node.model_dump(by_alias=True),
            'managementKey': sample_management_key.model_dump(by_alias=True),
            'challengeNonce': challenge_nonce,
            'challengeSolution': challenge_solution,
        }

        with pytest.raises(ValidationError):
            AuthInvite.model_validate(auth_invite_dict)

    def test_model_dump(self,
                        network_id,
                        node_id,
                        sample_network,
                        sample_node,
                        sample_management_key,
                        ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_invite = AuthInvite(
            metadata=metadata,
            network=sample_network,
            node=sample_node,
            managementKey=sample_management_key,
            challengeNonce=challenge_nonce,
            challengeSolution=challenge_solution,
        )

        auth_invite_dict = auth_invite.model_dump(by_alias=True)

        assert auth_invite_dict['metadata'] == metadata.model_dump(by_alias=True)
        assert auth_invite_dict['messageType'] == 'uk.co.firefox2100.ddg.auth.invite'
        assert auth_invite_dict['network'] == sample_network.model_dump(by_alias=True)
        assert auth_invite_dict['node'] == sample_node.model_dump(by_alias=True)
        assert auth_invite_dict['managementKey'] == sample_management_key.model_dump(by_alias=True)
        assert auth_invite_dict['challengeNonce'] == challenge_nonce
        assert auth_invite_dict['challengeSolution'] == challenge_solution

    def test_model_dump_json(self,
                             network_id,
                             node_id,
                             message_id,
                             timestamp,
                             sample_network,
                             sample_node,
                             sample_management_key,
                             ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
            messageId=message_id,
            timestamp=timestamp,
        )

        auth_invite = AuthInvite(
            metadata=metadata,
            network=sample_network,
            node=sample_node,
            managementKey=sample_management_key,
            challengeNonce=challenge_nonce,
            challengeSolution=challenge_solution,
        )

        auth_invite_json = auth_invite.model_dump_json(by_alias=True)

        expected_json = f'''{{"metadata":{{"networkId":"{network_id}","nodeId":"{node_id}",\
"messageId":"{message_id}","timestamp":{timestamp}}},\
"messageType":"uk.co.firefox2100.ddg.auth.invite",\
"node":{sample_node.model_dump_json()},\
"challengeNonce":"{challenge_nonce}",\
"challengeSolution":{challenge_solution},\
"justification":"",\
"network":{sample_network.model_dump_json()},\
"managementKey":{sample_management_key.model_dump_json()}}}'''

        assert auth_invite_json == expected_json

    def test_extra_field_validation(self,
                                    network_id,
                                    node_id,
                                    sample_network,
                                    sample_node,
                                    sample_management_key,
                                    ):
        challenge_nonce = 'nonce123'
        challenge_solution = 42

        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_invite_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_INVITE,
            'network': sample_network.model_dump(by_alias=True),
            'node': sample_node.model_dump(by_alias=True),
            'managementKey': sample_management_key.model_dump(by_alias=True),
            'challengeNonce': challenge_nonce,
            'challengeSolution': challenge_solution,
            'extraField': 'should not be here',
        }

        with pytest.raises(ValidationError):
            AuthInvite.model_validate(auth_invite_dict)
