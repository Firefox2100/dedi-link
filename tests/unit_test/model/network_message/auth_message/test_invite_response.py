from pydantic import ValidationError
import pytest

from dedi_link.etc.enums import MessageType
from dedi_link.model.network_message.message_metadata import MessageMetadata
from dedi_link.model.network_message.auth_message.invite_response import AuthInviteResponse


class TestAuthInviteResponse:
    def test_init(self,
                  network_id,
                  node_id,
                  sample_node,
                  ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_invite_response = AuthInviteResponse(
            metadata=metadata,
            approved=True,
            node=sample_node,
            justification='Looking forward to joining!',
        )

        assert auth_invite_response.metadata.network_id == network_id
        assert auth_invite_response.metadata.node_id == node_id
        assert auth_invite_response.message_type == MessageType.AUTH_INVITE_RESPONSE
        assert auth_invite_response.approved is True
        assert auth_invite_response.node == sample_node
        assert auth_invite_response.justification == 'Looking forward to joining!'

    def test_model_validate(self,
                            network_id,
                            node_id,
                            sample_node,
                            ):
        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_invite_response_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_INVITE_RESPONSE,
            'approved': True,
            'node': sample_node.model_dump(by_alias=True),
            'justification': 'Looking forward to joining!',
        }

        auth_invite_response = AuthInviteResponse.model_validate(auth_invite_response_dict)

        assert auth_invite_response.metadata.network_id == network_id
        assert auth_invite_response.metadata.node_id == node_id
        assert auth_invite_response.message_type == MessageType.AUTH_INVITE_RESPONSE
        assert auth_invite_response.approved is True
        assert auth_invite_response.node == sample_node
        assert auth_invite_response.justification == 'Looking forward to joining!'

    def test_model_validate_invalid_message_type(self,
                                                 network_id,
                                                 node_id,
                                                 sample_node,
                                                 ):
        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_invite_response_dict = {
            'metadata': metadata_dict,
            'messageType': 'INVALID_TYPE',
            'approved': True,
            'node': sample_node.model_dump(by_alias=True),
            'justification': 'Looking forward to joining!',
        }

        with pytest.raises(ValidationError) as exc_info:
            AuthInviteResponse.model_validate(auth_invite_response_dict)

        errors = exc_info.value.errors()
        assert any(
            error['type'] == 'literal_error' and error['loc'] == ('messageType',)
            for error in errors
        )

    def test_model_dump(self,
                        network_id,
                        node_id,
                        sample_node,
                        ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_invite_response = AuthInviteResponse(
            metadata=metadata,
            approved=True,
            node=sample_node,
            justification='Looking forward to joining!',
        )

        auth_invite_response_dict = auth_invite_response.model_dump()

        assert auth_invite_response_dict['metadata']['networkId'] == str(network_id)
        assert auth_invite_response_dict['metadata']['nodeId'] == str(node_id)
        assert auth_invite_response_dict['messageType'] == 'uk.co.firefox2100.ddg.auth.invite.response'
        assert auth_invite_response_dict['approved'] is True
        assert auth_invite_response_dict['node'] == sample_node.model_dump()
        assert auth_invite_response_dict['justification'] == 'Looking forward to joining!'

    def test_model_dump_json(self,
                             network_id,
                             node_id,
                             message_id,
                             timestamp,
                             sample_node,
                             ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
            messageId=message_id,
            timestamp=timestamp,
        )

        auth_invite_response = AuthInviteResponse(
            metadata=metadata,
            approved=True,
            node=sample_node,
            justification='Looking forward to joining!',
        )

        auth_invite_response_json = auth_invite_response.model_dump_json()

        expected_json = f'''{{"metadata":{{"networkId":"{network_id}","nodeId":"{node_id}",\
"messageId":"{message_id}","timestamp":{timestamp}}},\
"messageType":"uk.co.firefox2100.ddg.auth.invite.response",\
"approved":true,"node":{sample_node.model_dump_json()},"justification":"Looking forward to joining!"\
}}'''
        assert auth_invite_response_json == expected_json

    def test_extra_field_validation(self,
                                    network_id,
                                    node_id,
                                    sample_node,
                                    ):
        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_invite_response_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_INVITE_RESPONSE,
            'approved': True,
            'node': sample_node.model_dump(by_alias=True),
            'justification': 'Looking forward to joining!',
            'extraField': 'not allowed',
        }

        with pytest.raises(ValidationError) as exc_info:
            AuthInviteResponse.model_validate(auth_invite_response_dict)

        errors = exc_info.value.errors()
        assert any(
            error['type'] == 'extra_forbidden' and error['loc'] == ('extraField',)
            for error in errors
        )
