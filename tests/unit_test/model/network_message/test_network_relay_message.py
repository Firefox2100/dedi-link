import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import MessageType
from dedi_link.model.network_message.network_relay_message import RelayTarget, NetworkRelayMessage

from unit_test.consts import NODE_IDS, NETWORK_IDS


@pytest.fixture
def mock_relay_target_1(mock_network_message_header_1,
                        mock_auth_join_1,
                        ):
    return RelayTarget(
        recipient_ids=[NODE_IDS[5]],
        route=[NODE_IDS[0]],
        header=mock_network_message_header_1,
        message=mock_auth_join_1,
    )


@pytest.fixture
def mock_relay_target_dict_1(mock_network_message_header_dict_1,
                             mock_auth_join_dict_1,
                             ):
    return {
        'recipientIds': [NODE_IDS[5]],
        'route': [NODE_IDS[0]],
        'header': mock_network_message_header_dict_1,
        'message': mock_auth_join_dict_1,
    }


@pytest.fixture
def mock_relay_target_2(mock_network_message_header_1,
                        mock_auth_join_2,
                        ):
    return RelayTarget(
        recipient_ids=[NODE_IDS[9]],
        route=[NODE_IDS[0], NODE_IDS[6], NODE_IDS[8]],
        header=mock_network_message_header_1,
        message=mock_auth_join_2,
    )


@pytest.fixture
def mock_network_relay_message_1(mock_relay_target_1):
    return NetworkRelayMessage(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        relay_targets=[mock_relay_target_1],
        message_id='d8ded57b-1dc4-477c-9ada-b8d63c094846',
        timestamp=1704067200,
        ttl=3,
    )


@pytest.fixture
def mock_network_relay_message_dict_1(mock_relay_target_dict_1):
    return {
        'messageType': 'relayMessage',
        'messageAttributes': {
            'messageId': 'd8ded57b-1dc4-477c-9ada-b8d63c094846',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'ttl': 3,
        },
        'messageData':{
            'relayTargets': [mock_relay_target_dict_1],
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_network_relay_message_2(mock_relay_target_2):
    return NetworkRelayMessage(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        relay_targets=[mock_relay_target_2],
        message_id='f49d6dc4-3577-4d46-ac5b-781ae0fbf191',
        timestamp=1704067200,
        ttl=3,
    )


class TestRelayTarget:
    def test_init(self,
                  mock_network_message_header_1,
                  mock_auth_join_1,
                  ):
        relay_target = RelayTarget(
            recipient_ids=[NODE_IDS[5]],
            route=[NODE_IDS[0]],
            header=mock_network_message_header_1,
            message=mock_auth_join_1,
        )

        assert relay_target.recipient_ids == [NODE_IDS[5]]
        assert relay_target.route == [NODE_IDS[0]]
        assert relay_target.header == mock_network_message_header_1
        assert relay_target.message == mock_auth_join_1

    def test_equality(self,
                      mock_network_message_header_1,
                      mock_auth_join_1,
                      mock_relay_target_1,
                      mock_relay_target_2,
                      ):
        assert mock_relay_target_1 == RelayTarget(
            recipient_ids=[NODE_IDS[5]],
            route=[NODE_IDS[0]],
            header=mock_network_message_header_1,
            message=mock_auth_join_1,
        )

        assert mock_relay_target_1 != mock_relay_target_2

        assert mock_relay_target_1 != 'Random String'

    def test_hash(self,
                  mock_network_message_header_1,
                  mock_auth_join_1,
                  mock_relay_target_1,
                  ):
        assert hash(mock_relay_target_1) == hash(RelayTarget(
            recipient_ids=[NODE_IDS[5]],
            route=[NODE_IDS[0]],
            header=mock_network_message_header_1,
            message=mock_auth_join_1,
        ))

    def test_to_dict(self,
                     mock_relay_target_1,
                     mock_relay_target_dict_1,
                     ):
        assert not DeepDiff(
            mock_relay_target_1.to_dict(),
            mock_relay_target_dict_1,
            ignore_order=True,
        )

    def test_from_dict(self,
                       mock_relay_target_1,
                       mock_relay_target_dict_1,
                       ):
        assert RelayTarget.from_dict(mock_relay_target_dict_1) == mock_relay_target_1


class TestNetworkRelayMessage:
    def test_init(self,
                  mock_relay_target_1,
                  ):
        network_relay_message = NetworkRelayMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            relay_targets=[mock_relay_target_1],
            message_id='d8ded57b-1dc4-477c-9ada-b8d63c094846',
            timestamp=1704067200,
            ttl=3,
        )

        assert network_relay_message.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert network_relay_message.node_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_relay_message.relay_targets == [mock_relay_target_1]
        assert network_relay_message.message_id == 'd8ded57b-1dc4-477c-9ada-b8d63c094846'
        assert network_relay_message.timestamp == 1704067200
        assert network_relay_message.ttl == 3
        assert network_relay_message.message_type == MessageType.RELAY_MESSAGE

    def test_equality(self,
                      mock_relay_target_1,
                      mock_network_relay_message_1,
                      mock_network_relay_message_2,
                      ):
        assert mock_network_relay_message_1 == NetworkRelayMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            relay_targets=[mock_relay_target_1],
            message_id='d8ded57b-1dc4-477c-9ada-b8d63c094846',
            timestamp=1704067200,
            ttl=3,
        )

        assert mock_network_relay_message_1 != mock_network_relay_message_2

        assert mock_network_relay_message_1 != 'Random String'

    def test_hash(self,
                  mock_relay_target_1,
                  mock_network_relay_message_1,
                  ):
        assert hash(mock_network_relay_message_1) == hash(NetworkRelayMessage(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            relay_targets=[mock_relay_target_1],
            message_id='d8ded57b-1dc4-477c-9ada-b8d63c094846',
            timestamp=1704067200,
            ttl=3,
        ))

    def test_to_dict(self,
                     mock_network_relay_message_1,
                     mock_network_relay_message_dict_1,
                     ):
        assert not DeepDiff(
            mock_network_relay_message_1.to_dict(),
            mock_network_relay_message_dict_1,
            ignore_order=True,
        )

    def test_from_dict(self,
                       mock_network_relay_message_1,
                       mock_network_relay_message_dict_1,
                       ):
        assert NetworkRelayMessage.from_dict(mock_network_relay_message_dict_1) == mock_network_relay_message_1
