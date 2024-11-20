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


@pytest.mark.asyncio
class TestNetwork:
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

    async def test_network_unimplemented_methods(self, mock_network_1):
        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.nodes

        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.nodes_approved

        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.nodes_pending

        with pytest.raises(NetworkNotImplemented):
            _ = await mock_network_1.self_data_index

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
