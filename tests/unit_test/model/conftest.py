import pytest

from dedi_link.model import Network, Node, UserMapping, DataIndex


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
