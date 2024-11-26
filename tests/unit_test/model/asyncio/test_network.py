import pytest
from unittest.mock import patch, PropertyMock
from deepdiff import DeepDiff

from dedi_link.etc.exceptions import NetworkNotImplemented
from dedi_link.model.asyncio import Network, DataIndex, Node

from . import async_wrapper


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


class TestNetwork:
    def test_init(self):
        network = Network(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            network_name='Test Network',
            description='Test Description',
            node_ids=['86b0331a-c92a-44f9-9d3d-23b60e203838'],
            visible=True,
            instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
        )

        assert network.network_id == '62d13013-d80c-4539-adc1-61862bdd65cb'
        assert network.network_name == 'Test Network'
        assert network.description == 'Test Description'
        assert network.node_ids == ['86b0331a-c92a-44f9-9d3d-23b60e203838']
        assert network.visible is True
        assert network.instance_id == 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad'

    def test_equality(self, mock_network_1, mock_network_2):
        assert mock_network_1 == Network(
            network_id='62d13013-d80c-4539-adc1-61862bdd65cb',
            network_name='Test Network',
            description='Test Description',
            node_ids=['86b0331a-c92a-44f9-9d3d-23b60e203838'],
            visible=True,
            instance_id='f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
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

    @pytest.mark.asyncio
    async def test_to_dict_with_index(self, mock_network_1):
        with patch('dedi_link.model.asyncio.network.Network.network_data_index', new_callable=PropertyMock) as mock_data_index:
            mock_data_index.return_value = async_wrapper(DataIndex())

            payload = {
                'networkId': '62d13013-d80c-4539-adc1-61862bdd65cb',
                'networkName': 'Test Network',
                'description': 'Test Description',
                'nodeIds': ['86b0331a-c92a-44f9-9d3d-23b60e203838'],
                'visible': True,
                'instanceId': 'f3bb816f-608b-4dd7-ac74-8e0d0a0979ad',
                'dataIndex': {},
            }

            assert not DeepDiff(
                await mock_network_1.to_dict_with_index(),
                payload,
                ignore_order=True,
            )

    @pytest.mark.asyncio
    async def test_network_unimplemented_methods(self, mock_network_1):
        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.nodes

        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.nodes_approved

        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.nodes_pending

        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.self_data_index

    @pytest.mark.asyncio
    async def test_network_data_index(self, mock_network_1):
        with patch('dedi_link.model.asyncio.network.Network.nodes_approved', new_callable=PropertyMock) as mock_nodes:
            with patch('dedi_link.model.asyncio.network.Network.self_data_index', new_callable=PropertyMock) as mock_index:
                mock_nodes.return_value = async_wrapper([
                    Node(
                        node_id='cade9b4c-d3c4-4316-89a7-1ef1aec380fc',
                        node_name='Test Node',
                        url='https://test-node.com',
                        description='Test Description',
                        client_id='test-client-id',
                        data_index=DataIndex(),
                    )
                ])
                mock_index.return_value = async_wrapper(DataIndex())

                assert isinstance(await mock_network_1.network_data_index, DataIndex)
