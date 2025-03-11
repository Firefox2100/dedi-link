import json
import pytest
import networkx as nx
from unittest.mock import patch, PropertyMock, MagicMock
from cryptography.exceptions import InvalidSignature

from dedi_link.etc.enums import MappingType
from dedi_link.etc.exceptions import NetworkInterfaceNotImplemented, MessageAccessTokenInvalid
from dedi_link.model import Session, NetworkInterface, Network, UserMapping

from unit_test.consts import NODE_IDS


@pytest.fixture
def mock_network_interface(mock_ddl_config_1):
    with patch('dedi_link.model.base_model.BaseModel.config', new_callable=PropertyMock) as mock_config:
        mock_config.return_value = mock_ddl_config_1

        yield NetworkInterface(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        )


@pytest.fixture
def mock_network_graph_1():
    network_graph = nx.DiGraph()

    network_graph.add_nodes_from([
        (NODE_IDS[0], {'score': 0}),
        (NODE_IDS[1], {'score': 0.3}),
        (NODE_IDS[2], {'score': 0.5}),
        (NODE_IDS[3], {'score': 0.4}),
        (NODE_IDS[4], {'score': 0.6}),
        (NODE_IDS[5], {'score': 0.7}),
        (NODE_IDS[6], {'score': 0.2}),
        (NODE_IDS[7], {'score': 0.3}),
        (NODE_IDS[8], {'score': 0.5}),
        (NODE_IDS[9], {'score': 0.6}),
        (NODE_IDS[10], {'score': 0.1}),
        (NODE_IDS[11], {}),
    ])

    network_graph.add_edges_from([
        (NODE_IDS[0], NODE_IDS[1]),
        (NODE_IDS[1], NODE_IDS[0]),
        (NODE_IDS[0], NODE_IDS[2]),
        (NODE_IDS[3], NODE_IDS[0]),
        (NODE_IDS[0], NODE_IDS[6]),
        (NODE_IDS[2], NODE_IDS[4]),
        (NODE_IDS[4], NODE_IDS[3]),
        (NODE_IDS[3], NODE_IDS[4]),
        (NODE_IDS[2], NODE_IDS[5]),
        (NODE_IDS[1], NODE_IDS[5]),
        (NODE_IDS[5], NODE_IDS[1]),
        (NODE_IDS[6], NODE_IDS[7]),
        (NODE_IDS[6], NODE_IDS[8]),
        (NODE_IDS[8], NODE_IDS[7]),
        (NODE_IDS[8], NODE_IDS[9]),
        (NODE_IDS[9], NODE_IDS[10]),
    ])

    return network_graph


class TestNetworkInterface:
    def test_init(self,
                  mock_ddl_config_1,
                  ):
        session = Session()

        with patch('dedi_link.model.base_model.BaseModel.config', new_callable=PropertyMock) as mock_config:
            mock_config.return_value = mock_ddl_config_1

            network_interface = NetworkInterface(
                network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
                session=session,
            )

            assert network_interface.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
            assert network_interface.instance_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
            assert network_interface.config == mock_ddl_config_1
            assert network_interface.session == session

            interface_no_session = NetworkInterface(
                network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
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
        assert empty_url == f'{self_url}'

    def test_find_path_to_node(self,
                               mock_network_interface,
                               mock_network_graph_1,
                               ):
        # Long path but within threshold
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=NODE_IDS[9],
        )
        assert path == [
            [NODE_IDS[0], NODE_IDS[6], NODE_IDS[8], NODE_IDS[9]]
        ]

        # Multiple paths
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=NODE_IDS[5],
        )
        assert path == [
            [NODE_IDS[0], NODE_IDS[2], NODE_IDS[5]],
        ]

        # Path too long
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=NODE_IDS[10],
        )
        assert path == []

        # No path
        path = mock_network_interface._find_path_to_node(
            network_graph=mock_network_graph_1,
            node_id=NODE_IDS[11],
        )
        assert path == [
            [NODE_IDS[0], NODE_IDS[1], NODE_IDS[5]],
            [NODE_IDS[0], NODE_IDS[2], NODE_IDS[4]],
            [NODE_IDS[0], NODE_IDS[6], NODE_IDS[8], NODE_IDS[9]],
            [NODE_IDS[0], NODE_IDS[2]],
            [NODE_IDS[0], NODE_IDS[6], NODE_IDS[8]],
            [NODE_IDS[0], NODE_IDS[2], NODE_IDS[4], NODE_IDS[3]],
            [NODE_IDS[0], NODE_IDS[1]],
            [NODE_IDS[0], NODE_IDS[6], NODE_IDS[7]],
            [NODE_IDS[0], NODE_IDS[6]],
        ]

    def test_find_relay_nodes(self,
                              mock_network_interface,
                              mock_network_graph_1,
                              ):
        # Direct connection
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[NODE_IDS[1]],
        )
        assert relay_nodes == [NODE_IDS[1]]

        # Requires relaying
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[NODE_IDS[5]],
        )
        assert relay_nodes == [NODE_IDS[2]]

        # Multiple nodes on the same path
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[NODE_IDS[8], NODE_IDS[9]],
        )
        assert relay_nodes == [NODE_IDS[6]]

        # Multiple nodes on different paths
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[NODE_IDS[8], NODE_IDS[4]],
        )
        assert relay_nodes == [NODE_IDS[2], NODE_IDS[6]]

        # Multiple nodes with possible longer and merged paths
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[NODE_IDS[3], NODE_IDS[5]],
        )
        assert relay_nodes == [NODE_IDS[2]]

        # Unknown path
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[NODE_IDS[11]],
        )
        assert relay_nodes == [NODE_IDS[2], NODE_IDS[1], NODE_IDS[6]]

        # Path too long
        relay_nodes = mock_network_interface._find_relay_nodes(
            network_graph=mock_network_graph_1,
            node_ids=[NODE_IDS[10]],
        )
        assert relay_nodes == []

    def test_validate_signature(self,
                                mock_network_interface,
                                mock_public_key,
                                mock_private_key,
                                mock_auth_join_1,
                                ):
        mock_network = Network(
            network_id='',
            network_name='',
        )

        with patch('dedi_link.model.network.Network.load', return_value=mock_network):
            with patch('dedi_link.model.network.Network.private_key', new_callable=PropertyMock) as mock_p_key:
                mock_p_key.return_value = mock_private_key

                mock_signature = mock_auth_join_1.signature

        mock_network_interface._validate_signature(
            signature=mock_signature,
            payload=json.dumps(mock_auth_join_1.to_dict()).encode(),
            node_public_key=mock_public_key,
        )

        with pytest.raises(InvalidSignature):
            mock_network_interface._validate_signature(
                signature='Invalid Signature',
                payload=json.dumps(mock_auth_join_1.to_dict()).encode(),
                node_public_key=mock_public_key,
            )

    def test_validate_access_token(self,
                                   mock_network_interface,
                                   mock_oidc_registry,
                                   ):
        with patch('dedi_link.model.base_model.BaseModel.oidc',
                   new_callable=PropertyMock) as mock_oidc:
            mock_oidc.return_value = mock_oidc_registry

            user_id = mock_network_interface._validate_access_token(
                node_client_id='test_client_id',
                request_idp='https://mock-oidc.local',
                access_token='test_access_token',
            )

            assert user_id == '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb'
            mock_oidc_registry.default_driver.introspect_token.assert_called_once_with(
                'test_access_token'
            )

    def test_validate_access_token_exception(self,
                                             mock_network_interface,
                                             mock_oidc_registry,
                                             ):
        with patch('dedi_link.model.base_model.BaseModel.oidc',
                     new_callable=PropertyMock) as mock_oidc:
            mock_oidc.return_value = mock_oidc_registry

            with pytest.raises(MessageAccessTokenInvalid):
                # client ID mismatch
                _ = mock_network_interface._validate_access_token(
                    node_client_id='another_client_id',
                    request_idp='https://mock-oidc.local',
                    access_token='test_access_token',
                )

            with pytest.raises(MessageAccessTokenInvalid):
                # IdP unknown
                _ = mock_network_interface._validate_access_token(
                    node_client_id='client_id',
                    request_idp='https://another.mock-oidc.local',
                    access_token='test_access_token',
                )

            with pytest.raises(MessageAccessTokenInvalid):
                mock_oidc_registry.default_driver.introspect_token.return_value['active'] = False

                # Token not active
                _ = mock_network_interface._validate_access_token(
                    node_client_id='client_id',
                    request_idp='https://mock-oidc.local',
                    access_token='test_access_token',
                )

            # Error introspecting token
            mock_oidc_registry.default_driver.introspect_token.side_effect = Exception

            user_id = mock_network_interface._validate_access_token(
                    node_client_id='client_id',
                    request_idp='https://mock-oidc.local',
                    access_token='test_access_token',
                )
            assert user_id is None

    def test_calculate_new_score(self,
                                 mock_network_interface,
                                 ):
        new_score = mock_network_interface.calculate_new_score(
            time_elapsed=-1,
        )

        assert new_score == -1.0

        new_score = mock_network_interface.calculate_new_score(
            time_elapsed=10,
        )

        assert pytest.approx(new_score, 1e-4) == 0.6667

        new_score = mock_network_interface.calculate_new_score(
            time_elapsed=10,
            record_count=50,
            record_count_max=100,
        )

        assert pytest.approx(new_score, 1e-4) == 0.8333

        new_score = mock_network_interface.calculate_new_score(
            time_elapsed=10,
            record_count=95,
            record_count_max=100,
        )

        assert pytest.approx(new_score, 1e-4) == -0.15667

        with pytest.raises(ValueError):
            mock_network_interface.calculate_new_score(
                time_elapsed=10,
                record_count=150,
                record_count_max=100,
            )

    def test_context_manager(self,
                             mock_ddl_config_1,
                             ):
        with patch('dedi_link.model.base_model.BaseModel.config', new_callable=PropertyMock) as mock_config:
            mock_config.return_value = mock_ddl_config_1

            with NetworkInterface(
                network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
                instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
            ) as network_interface:
                assert network_interface.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
                assert network_interface.instance_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'
                assert network_interface.config == mock_ddl_config_1
                assert network_interface.session is not None
                assert isinstance(network_interface.session, Session)

    def test_network_graph(self,
                           mock_network_interface,
                           ):
        with pytest.raises(NetworkInterfaceNotImplemented):
            _ = mock_network_interface.network_graph

        with pytest.raises(NetworkInterfaceNotImplemented):
            with mock_network_interface.network_graph:
                pass

    def test_from_interface(self,
                            mock_network_interface,
                            ):
        new_interface = NetworkInterface.from_interface(mock_network_interface)

        assert new_interface.network_id == mock_network_interface.network_id
        assert new_interface.instance_id == mock_network_interface.instance_id
        assert new_interface.config == mock_network_interface.config
        assert new_interface.session == mock_network_interface.session

    def test_check_connectivity(self,
                                mock_client,
                                mock_network_interface,
                                ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'OK'}

        mock_client.return_value.get.return_value = mock_response

        # Local URL
        result = mock_network_interface.check_connectivity(
            url='http://localhost:5000'
        )
        assert not result

        # Self URL
        result = mock_network_interface.check_connectivity(
            url='https://test-node.example.com'
        )
        assert not result

        # External URL
        result = mock_network_interface.check_connectivity(
            url='https://example.com'
        )
        assert result

        # Request failed
        mock_client.return_value.get.side_effect = Exception

        result = mock_network_interface.check_connectivity(
            url='https://example.com'
        )
        assert not result
