from deepdiff import DeepDiff

from dedi_link.model import Node, UserMapping, DataIndex


class TestNode:
    def test_init(self):
        node = Node(
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

        assert node.node_id == '7961f714-421d-41b1-9ce5-08ef99bc4005'
        assert node.node_name == 'Test Node'
        assert node.url == 'https://node1.example.com'
        assert node.description == 'This is a test node'
        assert node.client_id == 'a04ffd6a-b93c-46d5-ac0e-54d59b32abb9'
        assert node.authentication_enabled == True
        assert node.user_mapping == UserMapping()
        assert node.public_key == 'test-public-key'
        assert node.data_index == DataIndex()
        assert node.score == 0

    def test_equality(self, mock_node_1, mock_node_2):
        assert mock_node_1 == Node(
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

        assert mock_node_1 != mock_node_2

        assert not mock_node_1 == 'Random String'

    def test_hash(self, mock_node_1):
        node_hash = hash(mock_node_1)

        assert isinstance(node_hash, int)

    def test_from_dict(self, mock_node_1, mock_node_dict_1):
        node = Node.from_dict(mock_node_dict_1)

        assert node == mock_node_1

    def test_to_dict(self, mock_node_1, mock_node_dict_1):
        node_dict = mock_node_1.to_dict(key=True)

        assert not DeepDiff(
            node_dict,
            mock_node_dict_1,
            ignore_order=True,
        )
