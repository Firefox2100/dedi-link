import pytest
import networkx as nx

from dedi_link.model import Session, NetworkInterface


@pytest.fixture
def mock_network_interface(mock_ddl_config_1):
    return NetworkInterface(
        network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
        instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        config=mock_ddl_config_1,
    )


@pytest.fixture
def node_id_map():
    return {
        0: 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        1: '895f4aa3-5336-4b75-8f74-5600dbc6f893',
        2: '61c03e05-e5a5-475f-8ad3-2b0f2168d8dc',
        3: 'eef7d34f-80f4-45a7-a9b9-e140e2a33b63',
        4: 'ef8a765c-ddb5-4f1a-b3c1-7d0230fb12e6',
        5: '9e19bc21-7e05-4ab0-82ea-26c5812fa8cd',
        6: '0cca72d5-a33b-4e5d-bef6-041f422ae81a',
        7: '542dffc0-2a1f-4c7c-b053-dba6d8addaa9',
        8: '8a50d2c6-ad04-4303-b316-0dbfa29efcd7',
        9: '5711e54a-12d4-45bd-85e4-32e3e50a77db',
        10: '48ef3be3-e2ee-451d-a9d6-32f6184037a1',
    }


@pytest.fixture
def mock_network_graph_1(node_id_map):
    network_graph = nx.DiGraph()

    network_graph.add_node(
        node_id_map[0],
        score=0,
    )
    network_graph.add_node(
        node_id_map[1],
        score=0.3,
    )
    network_graph.add_node(
        node_id_map[2],
        score=0.5,
    )
    network_graph.add_node(
        node_id_map[3],
        score=0.4,
    )
    network_graph.add_node(
        node_id_map[4],
        score=0.6,
    )
    network_graph.add_node(
        node_id_map[5],
        score=0.7,
    )
    network_graph.add_node(
        node_id_map[6],
        score=0.2,
    )
    network_graph.add_node(
        node_id_map[7],
        score=0.3,
    )
    network_graph.add_node(
        node_id_map[8],
        score=0.5,
    )
    network_graph.add_node(
        node_id_map[9],
        score=0.6,
    )
    network_graph.add_node(
        node_id_map[10],
    )

    network_graph.add_edge(
        node_id_map[0],
        node_id_map[1],
    )
    network_graph.add_edge(
        node_id_map[1],
        node_id_map[0],
    )
    network_graph.add_edge(
        node_id_map[0],
        node_id_map[2],
    )
    network_graph.add_edge(
        node_id_map[3],
        node_id_map[0],
    )
    network_graph.add_edge(
        node_id_map[0],
        node_id_map[6],
    )
    network_graph.add_edge(
        node_id_map[2],
        node_id_map[4],
    )
    network_graph.add_edge(
        node_id_map[4],
        node_id_map[3],
    )
    network_graph.add_edge(
        node_id_map[3],
        node_id_map[4],
    )
    network_graph.add_edge(
        node_id_map[2],
        node_id_map[5],
    )
    network_graph.add_edge(
        node_id_map[1],
        node_id_map[5],
    )
    network_graph.add_edge(
        node_id_map[5],
        node_id_map[1],
    )
    network_graph.add_edge(
        node_id_map[6],
        node_id_map[7],
    )
    network_graph.add_edge(
        node_id_map[6],
        node_id_map[8],
    )
    network_graph.add_edge(
        node_id_map[8],
        node_id_map[7],
    )
    network_graph.add_edge(
        node_id_map[8],
        node_id_map[9],
    )

    return network_graph


class TestNetworkInterface:
    def test_init(self, mock_ddl_config_1):
        session = Session()

        network_interface = NetworkInterface(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            config=mock_ddl_config_1,
            session=session,
        )

        assert network_interface.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert network_interface.instance_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert network_interface.config == mock_ddl_config_1
        assert network_interface.session == session

        interface_no_session = NetworkInterface(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            config=mock_ddl_config_1,
        )

        assert interface_no_session.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert interface_no_session.instance_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
        assert interface_no_session.config == mock_ddl_config_1
        assert interface_no_session.session is not None
        assert isinstance(interface_no_session.session, Session)
        assert interface_no_session.session != session

    def test_vote_from_responses(self, mock_network_interface):
        class TestingClass:
            def __init__(self,
                         object_id: str,
                         int_value: int,
                         str_value: str,
                         bool_value: bool,
                         ):
                self.object_id = object_id
                self.int_value = int_value
                self.str_value = str_value
                self.bool_value = bool_value

            def __eq__(self, other):
                return all([
                    self.object_id == other.object_id,
                    self.int_value == other.int_value,
                    self.str_value == other.str_value,
                    self.bool_value == other.bool_value,
                ])

            def __hash__(self):
                return hash((
                    self.object_id,
                    self.int_value,
                    self.str_value,
                    self.bool_value,
                ))

        test_objects = [
            [
                TestingClass('1', 1, '1', True),
            ],
            [
                TestingClass('1', 1, '1', True),
                TestingClass('2', 2, '2', False),
            ],
            [
                TestingClass('1', 1, '1', True),
            ],
            [
                TestingClass('1', 2, '1', False),
            ],
        ]

        voting_result = mock_network_interface.vote_from_responses(
            objects=test_objects,
            identifier='object_id',
            value_to_search='1',
        )

        assert voting_result == TestingClass('1', 1, '1', True)

    def test_check_connectivity_url(self, mock_network_interface):
        self_url = 'https://test-node.example.com'
        local_url = 'http://localhost:5000'

        assert mock_network_interface._check_connectivity_url(self_url) is None
        assert mock_network_interface._check_connectivity_url(local_url) is None

        empty_url = mock_network_interface._check_connectivity_url()
        assert empty_url == f'{self_url}/api'

    def test_find_path_to_node(self,
                               node_id_map,
                               mock_network_interface,
                               mock_network_graph_1,
                               ):
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=node_id_map[9],
        )

        assert path == [
            [
                node_id_map[0],
                node_id_map[6],
                node_id_map[8],
                node_id_map[9],
            ]
        ]

        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=node_id_map[10],
        )

        assert path == [
            [
                node_id_map[0],
                node_id_map[1],
                node_id_map[5],
            ],
            [
                node_id_map[0],
                node_id_map[2],
                node_id_map[4],
            ],
            [
                node_id_map[0],
                node_id_map[6],
                node_id_map[8],
                node_id_map[9],
            ],
            [
                node_id_map[0],
                node_id_map[2],
            ],
            [
                node_id_map[0],
                node_id_map[6],
                node_id_map[8],
            ],
            [
                node_id_map[0],
                node_id_map[2],
                node_id_map[4],
                node_id_map[3],
            ],
            [
                node_id_map[0],
                node_id_map[1],
            ],
            [
                node_id_map[0],
                node_id_map[6],
                node_id_map[7],
            ],
            [
                node_id_map[0],
                node_id_map[6],
            ]
        ]
