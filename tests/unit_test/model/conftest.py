import pytest
from unittest.mock import MagicMock

from dedi_link.etc.enums import AuthMessageStatus, SyncTarget
from dedi_link.model import Network, Node, UserMapping, DataIndex, DDLConfig, NetworkMessage
from dedi_link.model.network_message.network_message_header import NetworkMessageHeader
from dedi_link.model.network_message.network_auth_message import AuthRequest, AuthInvite, AuthResponse, AuthJoin, AuthLeave, \
    AuthStatus
from dedi_link.model.network_message.network_sync_message import NetworkSyncMessage

from unit_test.consts import NODE_IDS, NETWORK_IDS


@pytest.fixture
def mock_network_1():
    return Network(
        network_id=NETWORK_IDS[0],
        network_name='Test Network',
        description='Test Description',
        node_ids=[NODE_IDS[1]],
        visible=True,
        instance_id=NODE_IDS[0],
    )


@pytest.fixture
def mock_network_dict_1():
    return {
        'networkId': NETWORK_IDS[0],
        'networkName': 'Test Network',
        'description': 'Test Description',
        'nodeIds': [NODE_IDS[1]],
        'visible': True,
        'instanceId': NODE_IDS[0],
    }


@pytest.fixture
def mock_network_2():
    return Network(
        network_id=NETWORK_IDS[1],
        network_name='Test Network 2',
        description='Test Description 2',
        node_ids=[],
        visible=True,
        instance_id=NODE_IDS[12],
    )


@pytest.fixture
def mock_self_node_1():
    return Node(
        node_id=NODE_IDS[0],
        node_name='Test instance',
        url='https://test-node.example.com',
        description='This is a test instance',
        client_id='dedi-link',
        idp='https://mock-oidc.local',
        public_key='test-public-key',
    )


@pytest.fixture
def mock_self_node_dict_1():
    return {
        'nodeId': NODE_IDS[0],
        'nodeName': 'Test instance',
        'nodeUrl': 'https://test-node.example.com',
        'clientId': 'dedi-link',
        'idp': 'https://mock-oidc.local',
        'nodeDescription': 'This is a test instance',
        'publicKey': 'test-public-key',
        'score': 0.0,
        'approved': False,
        'authenticationEnabled': False,
    }


@pytest.fixture
def mock_node_1():
    return Node(
        node_id=NODE_IDS[1],
        node_name='Test Node',
        url='https://node1.example.com',
        description='This is a test node',
        client_id='a04ffd6a-b93c-46d5-ac0e-54d59b32abb9',
        idp='https://mock-oidc.local',
        authentication_enabled=True,
        user_mapping=UserMapping(),
        public_key='test-public-key',
        data_index=DataIndex(
            record_count=100,
        ),
        score=0.3,
    )


@pytest.fixture
def mock_node_dict_1():
    return {
        'nodeId': NODE_IDS[1],
        'nodeName': 'Test Node',
        'nodeUrl': 'https://node1.example.com',
        'nodeDescription': 'This is a test node',
        'clientId': 'a04ffd6a-b93c-46d5-ac0e-54d59b32abb9',
        'idp': 'https://mock-oidc.local',
        'authenticationEnabled': True,
        'approved': False,
        'publicKey': 'test-public-key',
        'dataIndex': {
            'recordCount': 100,
        },
        'score': 0.3,
    }


@pytest.fixture
def mock_node_2():
    return Node(
        node_id=NODE_IDS[2],
        node_name='Test Node 2',
        url='https://node2.example.com',
        description='This is a test node 2',
        client_id='f2827c56-758e-491d-829c-b86c7299b43f',
        idp='https://mock-oidc.local',
        authentication_enabled=False,
        user_mapping=UserMapping(),
        public_key='test-public-key-2',
        data_index=DataIndex(),
        score=0.5,
    )


@pytest.fixture
def mock_node_dict_2():
    return {
        'nodeId': NODE_IDS[2],
        'nodeName': 'Test Node 2',
        'nodeUrl': 'https://node2.example.com',
        'nodeDescription': 'This is a test node 2',
        'clientId': 'f2827c56-758e-491d-829c-b86c7299b43f',
        'idp': 'https://mock-oidc.local',
        'authenticationEnabled': False,
        'publicKey': 'test-public-key-2',
        'score': 0,
    }


@pytest.fixture
def mock_ddl_config_1():
    return DDLConfig(
        name='Test instance',
        description='This is a test instance',
        url='https://test-node.example.com',
        client_id='dedi-link',
        idp='https://mock-oidc.local',
        allow_non_client_authenticated=True,
        auto_user_registration=True,
        anonymous_access=True,
        default_ttl=3,
        optimal_record_percentage=0.5,
        time_score_weight=0.5,
        ema_factor=0.5,
    )


@pytest.fixture
def mock_network_message_header_1():
    return NetworkMessageHeader(
        node_id=NODE_IDS[0],
        network_id=NETWORK_IDS[0],
        server_signature='server_signature',
        access_token='access_token',
        user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
        delivered=True,
    )


@pytest.fixture
def mock_network_message_header_dict_1():
    return {
        'Content-Type': 'application/json',
        'X-Node-ID': NODE_IDS[0],
        'X-Network-ID': NETWORK_IDS[0],
        'X-Server-Signature': 'server_signature',
        'Authorization': 'Bearer access_token',
        'X-User-ID': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
        'X-Delivered': 'true',
    }


@pytest.fixture
def mock_network_message_header_2():
    return NetworkMessageHeader(
        node_id=NODE_IDS[12],
        network_id=NETWORK_IDS[1],
        server_signature='server_signature',
        access_token='access_token',
        user_id='9a05d3e5-7014-4416-ac2d-442cca395555',
        delivered=True,
    )


@pytest.fixture
def mock_network_message_1():
    return NetworkMessage(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        message_id='ef893ef0-1d29-4cae-ac61-0891f346fed3',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_network_message_2():
    return NetworkMessage(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        message_id='41b0a563-d0fe-46f4-ae43-813a36914a65',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_request_1(mock_self_node_1):
    return AuthRequest(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        status=AuthMessageStatus.SENT,
        node=mock_self_node_1,
        target_url='https://node1.example.com',
        challenge=['accident', 'flip', 'royal'],
        justification='This is a test',
        message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_request_dict_1(mock_self_node_dict_1):
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'authType': 'request',
            'targetUrl': 'https://node1.example.com',
            'status': 'sent',
        },
        'timestamp': 1704067200,
        'messageData': {
            'node': mock_self_node_dict_1,
            'challenge': ['accident', 'flip', 'royal'],
            'justification': 'This is a test',
        },
    }


@pytest.fixture
def mock_auth_request_2(mock_self_node_1, mock_network_1):
    return AuthRequest(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        status=AuthMessageStatus.SENT,
        node=mock_self_node_1,
        target_url='https://node2.example.com',
        challenge=['pluck', 'humor', 'music'],
        justification='This is a test',
        message_id='6669a5d8-7802-42a1-99a4-a303c0a4253c',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_request_dict_2(mock_self_node_dict_1):
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '6669a5d8-7802-42a1-99a4-a303c0a4253c',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'authType': 'request',
            'targetUrl': 'https://node2.example.com',
            'status': 'sent',
        },
        'messageData': {
            'node': mock_self_node_dict_1,
            'challenge': ['pluck', 'humor', 'music'],
            'justification': 'This is a test',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_response_1(mock_node_1, mock_network_1):
    return AuthResponse(
        message_id='a63c273c-bad2-4521-a7ce-5c9a4c07682d',
        approved=True,
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[1],
        node=mock_node_1,
        timestamp=1704067200,
        network=mock_network_1,
    )


@pytest.fixture
def mock_auth_response_dict_1(mock_node_dict_1, mock_network_dict_1):
    network_dict = mock_network_dict_1.copy()
    network_dict.pop('nodeIds')
    network_dict.pop('instanceId')

    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'a63c273c-bad2-4521-a7ce-5c9a4c07682d',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[1],
            'authType': 'response',
            'approved': True,
        },
        'messageData': {
            'node': mock_node_dict_1,
            'network': network_dict,
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_response_2():
    return AuthResponse(
        message_id='6669a5d8-7802-42a1-99a4-a303c0a4253c',
        approved=False,
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[2],
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_response_dict_2():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '6669a5d8-7802-42a1-99a4-a303c0a4253c',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[2],
            'authType': 'response',
            'approved': False,
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_join_1(mock_node_1):
    return AuthJoin(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
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
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'authType': 'join',
        },
        'timestamp': 1704067200,
        'messageData':{
            'node': mock_node_dict_1,
        },
    }


@pytest.fixture
def mock_auth_join_2(mock_node_2):
    return AuthJoin(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        node=mock_node_2,
        message_id='ddf9be31-319e-4592-8346-4cfd61a550fc',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_leave_1():
    return AuthLeave(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        message_id='32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_leave_dict_1():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': '32ee50ea-07e9-4667-9f0e-98b6fca8dfb4',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'authType': 'leave',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_leave_2():
    return AuthLeave(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        message_id='3edf7b0e-a811-43ee-b159-e75c22ed1d13',
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_1():
    return AuthStatus(
        message_id='fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_dict_1():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'fbdd4729-2a0d-4f99-8b6c-3ce08bafa091',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'authType': 'status',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_auth_status_2():
    return AuthStatus(
        message_id='b75c30a2-f7bd-46a3-87eb-bf871c48e0e9',
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
        status=AuthMessageStatus.ACCEPTED,
        timestamp=1704067200,
    )


@pytest.fixture
def mock_auth_status_dict_2():
    return {
        'messageType': 'authMessage',
        'messageAttributes': {
            'messageId': 'b75c30a2-f7bd-46a3-87eb-bf871c48e0e9',
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'authType': 'status',
            'status': 'accepted',
        },
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_network_sync_message_1(mock_node_1):
    return NetworkSyncMessage(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
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
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'targetType': 'node',
        },
        'messageData': [mock_node_dict_1],
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_network_sync_message_2(mock_node_1):
    return NetworkSyncMessage(
        network_id=NETWORK_IDS[0],
        node_id=NODE_IDS[0],
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
            'networkId': NETWORK_IDS[0],
            'nodeId': NODE_IDS[0],
            'targetType': 'user',
        },
        'messageData': [{
            'userId': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
            'publicKey': 'test_public_key',
        }],
        'timestamp': 1704067200,
    }


@pytest.fixture
def mock_public_key():
    return """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAjdXv5L1sjDnfK43Cwasd
q2cRDl3tJKbOJ97G2PdyCH0m27Ra28vsmijeMJnUZPYfatjoXgWPRbpR8cUwef/o
RcSbUAskvp+hcMEp6sTAP6IFcOLrltzMgjV2wT4WqP3Tkb6AZyvXDvGJSs0GdAl9
WL9SGOzk80BJNiAwDedPMwtxQWbk5nmP1RK9azgF6CQqaYohvv7jhNlZUElYW9eA
zQ/0I1RYDaIa5M6G/Z5ak32+3UM6f4wYqzA3nnpl6zPCi1Siuu57iNEM/EYel8uv
2skTCkl7zViQFr1Z9blAodhrMpaV3oyum9jczUcQ5gkTMn8VvQsrdCFvZbfPak7B
xrP/hDC9HWwit4DkpKjEpOszM99AxC6O/IEFLx0y09lFgv7V/OQQ3FKsjwimGnIe
XmQ9XRGvjMxuVjRW8gOeR6ypNegrcMoLmXiV3DLXnLonOiLyszTXs/xnmkFS7WHO
12K5PE7qIQZxf7kh6iR34HAng7MA0nOGPT3SkcE8VsC8A3Gs1by2mikKqsUN+Im4
OZm0AIYOz2/ytz7ArHkkfiwxzSSJ9f5YURsxFH0UH0mbbuDsMXOf+95t9s1uBSjX
pUzc/Rt0G8YErT1OkmvVG9y2xlhj/Mr1SujBab4jKMyM2sc3NMWsBqWkYT/YcWRf
j65o4mLG79hyNTpsfmRa5gECAwEAAQ==
-----END PUBLIC KEY-----
"""


@pytest.fixture
def mock_private_key():
    return """
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""


@pytest.fixture
def mock_oidc_driver():
    mock_driver = MagicMock()

    mock_driver.introspect_token.return_value = {
        'active': True,
        'client_id': 'test_client_id',
        'sub': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
    }

    mock_driver.exchange_token.return_value = 'new_access_token'

    return mock_driver
