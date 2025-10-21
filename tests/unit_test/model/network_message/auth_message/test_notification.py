from uuid import uuid4
from pydantic import ValidationError
import pytest

from dedi_link.etc.enums import MessageType, AuthNotificationType
from dedi_link.model.network_message.message_metadata import MessageMetadata
from dedi_link.model.network_message.auth_message.notification import AuthNotification


class TestAuthNotification:
    def test_init(self,
                  network_id,
                  node_id,
                  ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        affected_node_id = uuid4()

        auth_notification = AuthNotification(
            metadata=metadata,
            reason=AuthNotificationType.JOINING,
            affectedNodeId=affected_node_id,
        )

        assert auth_notification.metadata.network_id == network_id
        assert auth_notification.metadata.node_id == node_id
        assert auth_notification.message_type == MessageType.AUTH_NOTIFICATION
        assert auth_notification.reason == AuthNotificationType.JOINING
        assert auth_notification.affected_node_id == affected_node_id

    def test_model_validate(self,
                            network_id,
                            node_id,
                            ):
        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        affected_node_id = uuid4()

        auth_notification_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_NOTIFICATION,
            'reason': AuthNotificationType.LEAVING,
            'affectedNodeId': str(affected_node_id),
        }

        auth_notification = AuthNotification.model_validate(auth_notification_dict)

        assert auth_notification.metadata.network_id == network_id
        assert auth_notification.metadata.node_id == node_id
        assert auth_notification.message_type == MessageType.AUTH_NOTIFICATION
        assert auth_notification.reason == AuthNotificationType.LEAVING
        assert auth_notification.affected_node_id == affected_node_id

    def test_model_validate_invalid_message_type(self,
                                                 network_id,
                                                 node_id,
                                                 ):
        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        affected_node_id = uuid4()

        auth_notification_dict = {
            'metadata': metadata_dict,
            'messageType': 'INVALID_TYPE',
            'reason': AuthNotificationType.LEAVING,
            'affectedNodeId': str(affected_node_id),
        }

        with pytest.raises(ValidationError) as exc_info:
            AuthNotification.model_validate(auth_notification_dict)

        errors = exc_info.value.errors()
        assert errors[0]['type'] == 'literal_error'

    def test_model_validate_invalid_metadata(self,
                                             node_id,
                                             ):
        affected_node_id = uuid4()

        auth_notification_dict = {
            'metadata': {
                'networkId': 'invalid-uuid',
                'nodeId': str(node_id),
            },
            'messageType': MessageType.AUTH_NOTIFICATION,
            'reason': AuthNotificationType.LEAVING,
            'affectedNodeId': str(affected_node_id),
        }

        with pytest.raises(ValidationError) as exc_info:
            AuthNotification.model_validate(auth_notification_dict)

        errors = exc_info.value.errors()
        assert errors[0]['type'] == 'uuid_parsing'

    def test_model_dump(self,
                        network_id,
                        node_id,
                        ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        affected_node_id = uuid4()

        auth_notification = AuthNotification(
            metadata=metadata,
            reason=AuthNotificationType.JOINING,
            affectedNodeId=affected_node_id,
        )

        auth_notification_dict = auth_notification.model_dump(by_alias=True)

        assert auth_notification_dict['metadata']['networkId'] == str(network_id)
        assert auth_notification_dict['metadata']['nodeId'] == str(node_id)
        assert auth_notification_dict['messageType'] == 'uk.co.firefox2100.ddg.auth.notification'
        assert auth_notification_dict['reason'] == 'joining'
        assert auth_notification_dict['affectedNodeId'] == str(affected_node_id)

        assert 'messageId' in auth_notification_dict['metadata']
        assert 'timestamp' in auth_notification_dict['metadata']

    def test_model_dump_json(self,
                             network_id,
                             node_id,
                             message_id,
                             timestamp,
                             ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
            messageId=message_id,
            timestamp=timestamp,
        )

        affected_node_id = uuid4()

        auth_notification = AuthNotification(
            metadata=metadata,
            reason=AuthNotificationType.LEAVING,
            affectedNodeId=affected_node_id,
        )

        auth_notification_json = auth_notification.model_dump_json(by_alias=True)

        expected_json = f'''{{"metadata":{{"networkId":"{network_id}","nodeId":"{node_id}",\
"messageId":"{message_id}","timestamp":{timestamp}}},"messageType":"uk.co.firefox2100.ddg.auth.notification",\
"reason":"leaving","affectedNodeId":"{affected_node_id}\
}}'''
