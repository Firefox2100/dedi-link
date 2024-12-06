import json
import pytest
import networkx as nx
from cryptography.exceptions import InvalidSignature

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
        11: '24744a38-2c79-4e74-aebe-c3bcdd08dbd2',
    }


@pytest.fixture
def mock_network_graph_1(node_id_map):
    network_graph = nx.DiGraph()

    network_graph.add_nodes_from([
        (node_id_map[0], {'score': 0}),
        (node_id_map[1], {'score': 0.3}),
        (node_id_map[2], {'score': 0.5}),
        (node_id_map[3], {'score': 0.4}),
        (node_id_map[4], {'score': 0.6}),
        (node_id_map[5], {'score': 0.7}),
        (node_id_map[6], {'score': 0.2}),
        (node_id_map[7], {'score': 0.3}),
        (node_id_map[8], {'score': 0.5}),
        (node_id_map[9], {'score': 0.6}),
        (node_id_map[10], {'score': 0.1}),
        (node_id_map[11], {}),
    ])

    network_graph.add_edges_from([
        (node_id_map[0], node_id_map[1]),
        (node_id_map[1], node_id_map[0]),
        (node_id_map[0], node_id_map[2]),
        (node_id_map[3], node_id_map[0]),
        (node_id_map[0], node_id_map[6]),
        (node_id_map[2], node_id_map[4]),
        (node_id_map[4], node_id_map[3]),
        (node_id_map[3], node_id_map[4]),
        (node_id_map[2], node_id_map[5]),
        (node_id_map[1], node_id_map[5]),
        (node_id_map[5], node_id_map[1]),
        (node_id_map[6], node_id_map[7]),
        (node_id_map[6], node_id_map[8]),
        (node_id_map[8], node_id_map[7]),
        (node_id_map[8], node_id_map[9]),
        (node_id_map[9], node_id_map[10]),
    ])

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
        # Long path but within threshold
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=node_id_map[9],
        )
        assert path == [
            [node_id_map[0], node_id_map[6], node_id_map[8], node_id_map[9]]
        ]

        # Multiple paths
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=node_id_map[5],
        )
        assert path == [
            [node_id_map[0], node_id_map[2], node_id_map[5]],
        ]

        # Path too long
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=node_id_map[10],
        )
        assert path == []

        # No path
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=node_id_map[11],
        )
        assert path == [
            [node_id_map[0], node_id_map[1], node_id_map[5]],
            [node_id_map[0], node_id_map[2], node_id_map[4]],
            [node_id_map[0], node_id_map[6], node_id_map[8], node_id_map[9]],
            [node_id_map[0], node_id_map[2]],
            [node_id_map[0], node_id_map[6], node_id_map[8]],
            [node_id_map[0], node_id_map[2], node_id_map[4], node_id_map[3]],
            [node_id_map[0], node_id_map[1]],
            [node_id_map[0], node_id_map[6], node_id_map[7]],
            [node_id_map[0], node_id_map[6]],
        ]

    def test_find_relay_nodes(self,
                              node_id_map,
                              mock_network_interface,
                              mock_network_graph_1,
                              ):
        # Direct connection
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[node_id_map[1]],
        )
        assert relay_nodes == [node_id_map[1]]

        # Requires relaying
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[node_id_map[5]],
        )
        assert relay_nodes == [node_id_map[2]]

        # Multiple nodes on the same path
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[node_id_map[8], node_id_map[9]],
        )
        assert relay_nodes == [node_id_map[6]]

        # Multiple nodes on different paths
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[node_id_map[8], node_id_map[4]],
        )
        assert relay_nodes == [node_id_map[2], node_id_map[6]]

        # Multiple nodes with possible longer and merged paths
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[node_id_map[3], node_id_map[5]],
        )
        assert relay_nodes == [node_id_map[2]]

        # Unknown path
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[node_id_map[11]],
        )
        assert relay_nodes == [node_id_map[2], node_id_map[1], node_id_map[6]]

        # Path too long
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[node_id_map[10]],
        )
        assert relay_nodes == []

    def test_validate_signature(self,
                                mock_network_interface,
                                mock_public_key,
                                mock_network_message_dict_1,
                                ):
        mock_signature = (
            'Y/EbIkqRu9zj9K+t1OlJ6lia+ZTTQBFRA2fWaqGoKlBjdsLg7Z3SbvDNY'
            '8B9HiPnen8dgmxsRsuCw5JwL+4jFVIqcjDV0Ljx/Aid+eYDLf8FgkR5Vf'
            'DhaDxS1uduB9QXcdyWbfYHtYNDismdfJLrXCbNBE0bHwpo8Ug0fTmcKj2'
            'keQZCNFlWD61Ufp0iSXiHyIwsH1MUNRefm5XOuD7rYCN1UmLcgmpzBV3D'
            'TDwuQB6kRS5eypNhzEk4yOTpA6mr1JxDGi4F3Q/Osp2jvONLb36HRIk37'
            'kcRApv7F248LxsPLmBJKLrKQjgoF3MIK1ZzZB1Gki14Pd1AfBJRaFwE4p'
            'y/v/0D4vGYRGJ1GVl8qAOVFIC4myzYo8Wyn7YVcZ/y+HHlElJL0KaBgvE'
            'pypKrpUsFIMV62k371R+KnUJH4o16v76JaEOVLpypAWSJFaxdlbsm6ULZ'
            'rIalpTOVJeDQ7kG1Qo1CnbhbVhrFBcEeWa5DwVIa9FZfrmS2TE6lORwn1'
            'GhwoOR2D+nZUOt8A/H1Xl3FCjRlM8WfR9jantbsuhYvNGTzgQln87zNGI'
            'm1ukkxlWty44UMMk5HULfuGmHChbMkFYueiS3v+/ejPk7WJqnKTzBbp2X'
            '4dnvCKpu2wElMXahWm4/U4oc8OO9Fc1CA/+GoonLDQ2yBZUkiEJAFP2w='
        )

        mock_network_interface._validate_signature(
            signature=mock_signature,
            payload=json.dumps(mock_network_message_dict_1).encode(),
            node_public_key=mock_public_key,
        )

        with pytest.raises(InvalidSignature):
            mock_network_interface._validate_signature(
                signature='Invalid Signature',
                payload=json.dumps(mock_network_message_dict_1).encode(),
                node_public_key=mock_public_key,
            )
