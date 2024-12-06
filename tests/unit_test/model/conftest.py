import pytest

from dedi_link.etc.enums import MessageType, AuthMessageType, AuthMessageStatus, SyncTarget
from dedi_link.model import Network, Node, UserMapping, DataIndex
from dedi_link.model.network_message.network_message_header import NetworkMessageHeader
from dedi_link.model.network_message.network_auth_message import AuthRequestInvite, AuthResponse, AuthJoin, AuthLeave, \
    AuthStatus
from dedi_link.model.network_message.network_sync_message import NetworkSyncMessage


@pytest.fixture
def mock_network_1():
    return Network(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        network_name='Test Network',
        description='Test Description',
        node_ids=['86b0331a-c92a-44f9-9d3d-23b60e203838'],
        visible=True,
        instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
    )


@pytest.fixture
def mock_network_dict_1():
    return {
        'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
        'networkName': 'Test Network',
        'description': 'Test Description',
        'nodeIds': ['86b0331a-c92a-44f9-9d3d-23b60e203838'],
        'visible': True,
        'instanceId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
    }


@pytest.fixture
def mock_network_2():
    return Network(
        network_id='428fa5a2-132f-4a9e-981a-cad16ae702db',
        network_name='Test Network 2',
        description='Test Description 2',
        node_ids=['20b6b2dd-b21d-49e4-ba2b-4a92fe1ba348'],
        visible=True,
        instance_id='dbc92bce-e74a-4f9c-b53a-5d41c1611872',
    )


@pytest.fixture
def mock_node_1():
    return Node(
        node_id='7961f714-421d-41b1-9ce5-08ef99bc4005',
        node_name='Test Node',
        url='https://node1.example.com',
        description='This is a test node',
        client_id='a04ffd6a-b93c-46d5-ac0e-54d59b32abb9',
        authentication_enabled=True,
        user_mapping=UserMapping(),
        public_key='test-public-key',
        data_index=DataIndex(),
        score=0,
    )


@pytest.fixture
def mock_node_dict_1():
    return {
        'nodeId': '7961f714-421d-41b1-9ce5-08ef99bc4005',
        'nodeName': 'Test Node',
        'nodeUrl': 'https://node1.example.com',
        'nodeDescription': 'This is a test node',
        'clientId': 'a04ffd6a-b93c-46d5-ac0e-54d59b32abb9',
        'authenticationEnabled': True,
        'publicKey': 'test-public-key',
        'dataIndex': {},
        'score': 0,
    }


@pytest.fixture
def mock_node_2():
    return Node(
        node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
        node_name='Test Node 2',
        url='https://node2.example.com',
        description='This is a test node 2',
        client_id='f2827c56-758e-491d-829c-b86c7299b43f',
        authentication_enabled=False,
        user_mapping=UserMapping(),
        public_key='test-public-key-2',
        data_index=DataIndex(),
        score=0,
    )


@pytest.fixture
def mock_node_dict_2():
    return {
        'nodeId': 'd3398f33-e621-465c-846f-f7f79dff6a87',
        'nodeName': 'Test Node 2',
        'nodeUrl': 'https://node2.example.com',
        'nodeDescription': 'This is a test node 2',
        'clientId': 'f2827c56-758e-491d-829c-b86c7299b43f',
        'authenticationEnabled': False,
        'publicKey': 'test-public-key-2',
        'dataIndex': {},
        'score': 0,
    }


@pytest.fixture
def mock_network_message_header_1():
    return NetworkMessageHeader(
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        server_signature='server_signature',
        access_token='access_token',
        user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
        delivered=True,
    )


@pytest.fixture
def mock_network_message_header_dict_1():
    return {
        'Content-Type': 'application/json',
        'X-Node-ID': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        'X-Network-ID': '62d13013-d80c-4539-adc1-61862bdd65cb',
        'X-Server-Signature': 'server_signature',
        'Authorization': 'Bearer access_token',
        'X-User-ID': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
        'X-Delivered': 'true',
    }


@pytest.fixture
def mock_network_message_header_2():
    return NetworkMessageHeader(
        node_id='428fa5a2-132f-4a9e-981a-cad16ae702db',
        network_id='1560cbf8-29e4-4fee-af31-b88ebe61e440',
        server_signature='server_signature',
        access_token='access_token',
        user_id='9a05d3e5-7014-4416-ac2d-442cca395555',
        delivered=True,
    )


@pytest.fixture
def mock_auth_request_invite_1(mock_node_1):
    return AuthRequestInvite(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        auth_type=AuthMessageType.REQUEST,
        status=AuthMessageStatus.SENT,
        node=mock_node_1,
        target_url='https://node2.example.com',
        challenge=['accident', 'flip', 'royal'],
        justification='This is a test',
        message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_request_invite_dict_1(mock_node_dict_1):
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'request',
            'targetUrl': 'https://node2.example.com',
            'status': 'sent',
        },
        'messageData': {
            'node': mock_node_dict_1,
            'challenge': ['accident', 'flip', 'royal'],
            'justification': 'This is a test',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_request_invite_2(mock_node_1, mock_network_1):
    return AuthRequestInvite(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        auth_type=AuthMessageType.INVITE,
        status=AuthMessageStatus.SENT,
        node=mock_node_1,
        target_url='https://node2.example.com',
        challenge=['pluck', 'humor', 'music'],
        justification='This is a test',
        message_id='6669a5d8-7802-42a1-99a4-a303c0a4253c',
        timestamp=1704067200,
        network=mock_network_1,
    )


@pytest.fixture
def mock_auth_request_invite_dict_2(mock_node_dict_1, mock_network_dict_1):
    network_dict = mock_network_dict_1.copy()
    network_dict.pop('nodeIds')
    network_dict.pop('instanceId')

    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '6669a5d8-7802-42a1-99a4-a303c0a4253c',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'invite',
            'targetUrl': 'https://node2.example.com',
            'status': 'sent',
        },
        'messageData': {
            'node': mock_node_dict_1,
            'network': network_dict,
            'challenge': ['pluck', 'humor', 'music'],
            'justification': 'This is a test',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_response_1(mock_node_2, mock_network_1):
    return AuthResponse(
        message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
        approved=True,
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
        node=mock_node_2,
        timestamp=1704067200,
        network=mock_network_1,
    )


@pytest.fixture
def mock_auth_response_dict_1(mock_node_dict_2, mock_network_dict_1):
    network_dict = mock_network_dict_1.copy()
    network_dict.pop('nodeIds')
    network_dict.pop('instanceId')

    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'd3398f33-e621-465c-846f-f7f79dff6a87',
            'authType': 'response',
            'approved': True,
        },
        'messageData': {
            'node': mock_node_dict_2,
            'network': network_dict,
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_response_2():
    return AuthResponse(
        message_id='6669a5d8-7802-42a1-99a4-a303c0a4253c',
        approved=False,
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='d3398f33-e621-465c-846f-f7f79dff6a87',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_response_dict_2():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '6669a5d8-7802-42a1-99a4-a303c0a4253c',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'd3398f33-e621-465c-846f-f7f79dff6a87',
            'authType': 'response',
            'approved': False,
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_join_1(mock_node_1):
    return AuthJoin(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        node=mock_node_1,
        message_id='1be8938b-f656-4c8b-9e45-93c84af95723',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_join_dict_1(mock_node_dict_1):
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '1be8938b-f656-4c8b-9e45-93c84af95723',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'join',
        },
        'messageData':{
            'node': mock_node_dict_1,
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_join_2(mock_node_2):
    return AuthJoin(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        node=mock_node_2,
        message_id='ddf9be31-319e-4592-8346-4cfd61a550fc',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_leave_1():
    return AuthLeave(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        message_id='32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_leave_dict_1():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'leave',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_leave_2():
    return AuthLeave(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        message_id='3edf7b0e-a811-43ee-b159-e75c22ed1d13',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_1():
    return AuthStatus(
        message_id='fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_dict_1():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'status',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_status_2():
    return AuthStatus(
        message_id='b75c30a2-f7bd-46a3-87eb-bf871c48e0e9',
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        node_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        status=AuthMessageStatus.ACCEPTED,
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_dict_2():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'b75c30a2-f7bd-46a3-87eb-bf871c48e0e9',
            'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
            'nodeId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            'authType': 'status',
            'status': 'accepted',
        },
        'timestamp': 1704067200,
    }


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
