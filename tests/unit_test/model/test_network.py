import pytest
from unittest.mock import patch, PropertyMock
from deepdiff import DeepDiff

from dedi_link.etc.exceptions import NetworkNotImplemented
from dedi_link.model import Network, DataIndex

from unit_test.consts import NETWORK_IDS, NODE_IDS


class TestNetwork:
    def test_init(self):
        network = Network(
            network_id=NETWORK_IDS[0],
            network_name='Test Network',
            description='Test Description',
            node_ids=[NODE_IDS[1]],
            visible=True,
            instance_id=NODE_IDS[0],
        )

        assert network.network_id == NETWORK_IDS[0]
        assert network.network_name == 'Test Network'
        assert network.description == 'Test Description'
        assert network.node_ids == [NODE_IDS[1]]
        assert network.visible is True
        assert network.instance_id == NODE_IDS[0]

    def test_equality(self, mock_network_1, mock_network_2):
        assert mock_network_1 == Network(
            network_id=NETWORK_IDS[0],
            network_name='Test Network',
            description='Test Description',
            node_ids=[NODE_IDS[1]],
            visible=True,
            instance_id=NODE_IDS[0],
        )
        assert mock_network_1 != mock_network_2

        assert not mock_network_1 == 'Random Object'

    def test_hash(self, mock_network_1):
        network_hash = hash(mock_network_1)
        assert isinstance(network_hash, int)

    def test_from_dict(self, mock_network_1, mock_network_dict_1):
        network = Network.from_dict(mock_network_dict_1)

        assert network == mock_network_1

    def test_from_dict_missing_id(self, mock_network_dict_1):
        payload = mock_network_dict_1.copy()
        payload.pop('networkId')
        payload.pop('instanceId')

        network = Network.from_dict(payload)

        assert network.network_id is not None
        assert network.network_id != ''
        assert network.network_id != '62d13013-d80c-4539-adc1-61862bdd65cb'

        assert network.instance_id is not None
        assert network.instance_id != ''
        assert network.instance_id != 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'

    def test_to_dict(self, mock_network_1, mock_network_dict_1):
        assert not DeepDiff(
            mock_network_1.to_dict(),
            mock_network_dict_1,
            ignore_order=True,
        )

    def test_to_dict_with_index(self, mock_network_1, mock_network_dict_1):
        with patch(
                'dedi_link.model.network.Network.network_data_index',
                new_callable=PropertyMock,
        ) as mock_data_index:
            mock_data_index.return_value = DataIndex()

            payload = mock_network_dict_1.copy()
            payload['dataIndex'] = {}

            assert not DeepDiff(
                mock_network_1.to_dict_with_index(),
                payload,
                ignore_order=True,
            )

    def test_network_unimplemented_methods(self, mock_network_1):
        with pytest.raises(NetworkNotImplemented):
            _ = mock_network_1.nodes

        with pytest.raises(NetworkNotImplemented):
            _ = mock_network_1.nodes_approved

        with pytest.raises(NetworkNotImplemented):
            _ = mock_network_1.nodes_pending

        with pytest.raises(NetworkNotImplemented):
            _ = mock_network_1.self_data_index

    def test_network_data_index(self, mock_network_1, mock_node_1):
        with patch('dedi_link.model.network.Network.nodes_approved', new_callable=PropertyMock) as mock_nodes:
            with patch('dedi_link.model.network.Network.self_data_index', new_callable=PropertyMock) as mock_index:
                mock_nodes.return_value = [
                    mock_node_1,
                ]
                mock_index.return_value = DataIndex()

                assert isinstance(mock_network_1.network_data_index, DataIndex)

    def test_public_key(self, mock_network_1):
        with pytest.raises(NetworkNotImplemented):
            _ = mock_network_1.public_key

    def test_private_key(self, mock_network_1):
        with pytest.raises(NetworkNotImplemented):
            _ = mock_network_1.private_key

    def test_generate_keys(self, mock_network_1):
        with pytest.raises(NetworkNotImplemented):
            mock_network_1.generate_keys()

    def test_get_self_node(self,
                           mock_ddl_config_1,
                           mock_network_1,
                           mock_self_node_1,
                           ):
        with patch('dedi_link.model.network.Network.public_key', new_callable=PropertyMock) as mock_pub_key:
            mock_pub_key.return_value = 'test-public-key'

            self_node = mock_network_1.get_self_node(mock_ddl_config_1)

            assert self_node == mock_self_node_1
