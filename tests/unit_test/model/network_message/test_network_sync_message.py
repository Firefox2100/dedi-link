import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import MessageType, SyncTarget
from dedi_link.model.network_message import NetworkSyncMessage


@pytest.fixture
def mock_network_sync_message_1(mock_node_1):
    return NetworkSyncMessage(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        target_type=SyncTarget.NODE,
        data=[mock_node_1],
        message_id='afc42b81-68ab-472b-8489-8bede573a4b7',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_network_sync_message_dict_1(mock_node_dict_1):
    return {
        'messageType': 'syncMessage',
        'messageAttributes': {
            'messageId': 'afc42b81-68ab-472b-8489-8bede573a4b7',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'targetType': 'node',
        },
        'messageData': [mock_node_dict_1],
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_network_sync_message_2(mock_node_1):
    return NetworkSyncMessage(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        target_type=SyncTarget.USER,
        data=[{
            'userId': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            'publicKey': 'test_public_key',
        }],
        message_id='11bd629c-2d90-48f2-b176-6b9e10a4dcc5',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_network_sync_message_dict_2():
    return {
        'messageType': 'syncMessage',
        'messageAttributes': {
            'messageId': '11bd629c-2d90-48f2-b176-6b9e10a4dcc5',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'targetType': 'user',
        },
        'messageData': [{
            'userId': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            'publicKey': 'test_public_key',
        }],
        'timestamp': 1704067200,
    }


class TestNetworkSyncMessage:
    def test_init(self, mock_node_1):
        network_sync_message = NetworkSyncMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            target_type=SyncTarget.NODE,
            data=[mock_node_1],
            message_id='afc42b81-68ab-472b-8489-8bede573a4b7',
            timestamp=1704067200,
        )

        assert network_sync_message.message_type == MessageType.SYNC_MESSAGE
        assert network_sync_message.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert network_sync_message.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_sync_message.target_type == SyncTarget.NODE
        assert network_sync_message.data == [mock_node_1]
        assert network_sync_message.message_id == 'afc42b81-68ab-472b-8489-8bede573a4b7'
        assert network_sync_message.timestamp == 1704067200

    def test_equality(self,
                      mock_node_1,
                      mock_network_sync_message_1,
                      mock_network_sync_message_2,
                      ):
        assert mock_network_sync_message_1 == NetworkSyncMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            target_type=SyncTarget.NODE,
            data=[mock_node_1],
            message_id='afc42b81-68ab-472b-8489-8bede573a4b7',
            timestamp=1704067200,
        )

        assert mock_network_sync_message_1 != mock_network_sync_message_2

        assert mock_network_sync_message_1 != 'Random String'

    def test_hash(self, mock_network_sync_message_1):
        message_hash = hash(mock_network_sync_message_1)

        assert isinstance(message_hash, int)

    def test_to_dict(self,
                     mock_network_sync_message_1,
                     mock_network_sync_message_2,
                     mock_network_sync_message_dict_1,
                     mock_network_sync_message_dict_2,
                     ):
        assert not DeepDiff(
            mock_network_sync_message_1.to_dict(),
            mock_network_sync_message_dict_1,
            ignore_order=True,
        )
        assert not DeepDiff(
            mock_network_sync_message_2.to_dict(),
            mock_network_sync_message_dict_2,
            ignore_order=True,
        )

    def test_from_dict(self,
                       mock_network_sync_message_1,
                       mock_network_sync_message_2,
                       mock_network_sync_message_dict_1,
                       mock_network_sync_message_dict_2,
                       ):
        network_sync_message_1 = NetworkSyncMessage.from_dict(mock_network_sync_message_dict_1)
        network_sync_message_2 = NetworkSyncMessage.from_dict(mock_network_sync_message_dict_2)

        assert network_sync_message_1 == mock_network_sync_message_1
        assert network_sync_message_2 == mock_network_sync_message_2
