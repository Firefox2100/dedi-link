from pydantic import ValidationError
import pytest

from dedi_link.etc.enums import MessageType
from dedi_link.model.network_message.message_metadata import MessageMetadata
from dedi_link.model.network_message.auth_message.connect import AuthConnect


class TestAuthConnect:
    def test_init(self,
                  network_id,
                  node_id,
                  ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_connect = AuthConnect(
            metadata=metadata,
        )

        assert auth_connect.metadata.network_id == network_id
        assert auth_connect.metadata.node_id == node_id
        assert auth_connect.message_type == MessageType.AUTH_CONNECT

    def test_model_validate(self,
                            network_id,
                            node_id,
                            ):
        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_connect_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_CONNECT,
        }

        auth_connect = AuthConnect.model_validate(auth_connect_dict)

        assert auth_connect.metadata.network_id == network_id
        assert auth_connect.metadata.node_id == node_id
        assert auth_connect.message_type == MessageType.AUTH_CONNECT

    def test_model_validate_invalid_message_type(self,
                                                 network_id,
                                                 node_id,
                                                 ):
        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_connect_dict = {
            'metadata': metadata_dict,
            'messageType': 'INVALID_TYPE',
        }

        with pytest.raises(ValidationError):
            AuthConnect.model_validate(auth_connect_dict)

    def test_model_validate_invalid_metadata(self,
                                             node_id,
                                             ):
        auth_connect_dict = {
            'metadata': {
                'networkId': 'invalid-uuid',
                'nodeId': str(node_id),
            },
            'messageType': MessageType.AUTH_CONNECT,
        }

        with pytest.raises(ValidationError):
            AuthConnect.model_validate(auth_connect_dict)

    def test_model_dump(self,
                        network_id,
                        node_id,
                        ):
        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        auth_connect = AuthConnect(
            metadata=metadata,
        )

        auth_connect_dict = auth_connect.model_dump(by_alias=True)

        assert auth_connect_dict['metadata']['networkId'] == str(network_id)
        assert auth_connect_dict['metadata']['nodeId'] == str(node_id)
        assert auth_connect_dict['messageType'] == 'uk.co.firefox2100.ddg.auth.connect'

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

        auth_connect = AuthConnect(
            metadata=metadata,
        )

        auth_connect_json = auth_connect.model_dump_json(by_alias=True)

        expected_json = f'''{{"metadata":{{"networkId":"{network_id}","nodeId":"{node_id}",\
"messageId":"{message_id}","timestamp":{timestamp}}},"messageType":"uk.co.firefox2100.ddg.auth.connect"\
}}'''

        assert auth_connect_json == expected_json
