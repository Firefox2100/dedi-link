from pydantic import ValidationError
import pytest

from dedi_link.etc.enums import MessageType
from dedi_link.model.network_message.message_metadata import MessageMetadata
from dedi_link.model.network_message.auth_message.request_response import AuthRequestResponse


class TestAuthRequestResponse:
    def test_init(self,
                  network_id,
                  node_id,
                  sample_network,
                  sample_node,
                  sample_management_key,
                  ):
        justification = 'Welcome to the network!'

        auth_request_response = AuthRequestResponse(
            metadata=MessageMetadata(
                networkId=network_id,
                nodeId=node_id,
            ),
            approved=True,
            node=sample_node,
            justification=justification,
            network=sample_network,
            managementKey=sample_management_key,
        )

        assert auth_request_response.metadata.network_id == network_id
        assert auth_request_response.metadata.node_id == node_id
        assert auth_request_response.message_type == MessageType.AUTH_REQUEST_RESPONSE
        assert auth_request_response.approved == True
        assert auth_request_response.network == sample_network
        assert auth_request_response.node == sample_node
        assert auth_request_response.justification == justification
        assert auth_request_response.management_key == sample_management_key

    def test_model_validate(self,
                            network_id,
                            node_id,
                            sample_network,
                            sample_node,
                            sample_management_key,
                            ):
        justification = 'Welcome to the network!'

        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
        }

        auth_request_response_dict = {
            'metadata': metadata_dict,
            'messageType': MessageType.AUTH_REQUEST_RESPONSE,
            'approved': True,
            'node': sample_node.model_dump(),
            'justification': justification,
            'network': sample_network.model_dump(),
            'managementKey': sample_management_key.model_dump(),
        }

        auth_request_response = AuthRequestResponse.model_validate(
            auth_request_response_dict
        )

        assert auth_request_response.metadata.network_id == network_id
        assert auth_request_response.metadata.node_id == node_id
        assert auth_request_response.message_type == MessageType.AUTH_REQUEST_RESPONSE
        assert auth_request_response.approved == True
        assert auth_request_response.network == sample_network
        assert auth_request_response.node == sample_node
        assert auth_request_response.justification == justification
        assert auth_request_response.management_key == sample_management_key

    def test_model_dump(self,
                        network_id,
                        node_id,
                        sample_network,
                        sample_node,
                        sample_management_key,
                        ):
        justification = 'Welcome to the network!'

        auth_request_response = AuthRequestResponse(
            metadata=MessageMetadata(
                networkId=network_id,
                nodeId=node_id,
            ),
            approved=True,
            node=sample_node,
            justification=justification,
            network=sample_network,
            managementKey=sample_management_key,
        )

        auth_request_response_dict = auth_request_response.model_dump()

        assert auth_request_response_dict['metadata']['networkId'] == str(network_id)
        assert auth_request_response_dict['metadata']['nodeId'] == str(node_id)
        assert auth_request_response_dict['messageType'] == 'uk.co.firefox2100.ddg.auth.request.response'
        assert auth_request_response_dict['approved'] == True
        assert auth_request_response_dict['network'] == sample_network.model_dump()
        assert auth_request_response_dict['node'] == sample_node.model_dump()
        assert auth_request_response_dict['managementKey'] == sample_management_key.model_dump()

    def test_model_dump_json(self,
                             network_id,
                             node_id,
                             message_id,
                             timestamp,
                             sample_network,
                             sample_node,
                             sample_management_key,
                             ):
        justification = 'Welcome to the network!'
        auth_request_response = AuthRequestResponse(
            metadata=MessageMetadata(
                networkId=network_id,
                nodeId=node_id,
                messageId=message_id,
                timestamp=timestamp,
            ),
            approved=True,
            node=sample_node,
            justification=justification,
            network=sample_network,
            managementKey=sample_management_key,
        )

        auth_request_response_json = auth_request_response.model_dump_json()

        expected_json = f'''{{"metadata":{{"networkId":"{network_id}","nodeId":"{node_id}",\
"messageId":"{message_id}","timestamp":{timestamp}}},"messageType":\
"uk.co.firefox2100.ddg.auth.request.response","approved":true,"node":\
{sample_node.model_dump_json()},"justification":"{justification}",\
"network":{sample_network.model_dump_json()},"managementKey":{sample_management_key.model_dump_json()}\
}}'''

        assert auth_request_response_json == expected_json
