from uuid import uuid4, UUID
from pydantic import ValidationError
import pytest

from dedi_link.model.network import Network


class TestNetwork:
    def test_init(self):
        network_id = uuid4()
        node_id = uuid4()
        instance_id = uuid4()
        central_node = uuid4()

        network = Network(
            networkId=network_id,
            networkName='Test Network',
            description='A test network for unit testing.',
            nodeIds=[node_id],
            visible=True,
            registered=True,
            instanceId=instance_id,
            centralNode=central_node,
        )

        assert network.network_id == network_id
        assert network.network_name == 'Test Network'
        assert network.description == 'A test network for unit testing.'
        assert network.node_ids == [node_id]
        assert network.visible is True
        assert network.registered is True
        assert network.instance_id == instance_id
        assert network.central_node == central_node

        network = Network(
            networkName='Test Network',
            description='A test network for unit testing.',
        )

        assert isinstance(network.network_id, UUID)
        assert network.node_ids == []
        assert network.visible is False
        assert network.registered is False
        assert isinstance(network.instance_id, UUID)
        assert network.central_node is None

    def test_model_validate(self):
        network_id = uuid4()
        node_id = uuid4()
        instance_id = uuid4()
        central_node = uuid4()

        network_dict = {
            'networkId': str(network_id),
            'networkName': 'Test Network',
            'description': 'A test network for unit testing.',
            'nodeIds': [str(node_id)],
            'visible': True,
            'registered': True,
            'instanceId': str(instance_id),
            'centralNode': str(central_node),
        }

        network = Network.model_validate(network_dict)

        assert network.network_id == network_id
        assert network.network_name == 'Test Network'
        assert network.description == 'A test network for unit testing.'
        assert network.node_ids == [node_id]
        assert network.visible is True
        assert network.registered is True
        assert network.instance_id == instance_id
        assert network.central_node == central_node

    def test_model_validate_error(self):
        network_dict = {
            'networkId': 'invalid-uuid',
            'networkName': 'Test Network',
        }

        with pytest.raises(ValidationError):
            Network.model_validate(network_dict)

    def test_model_dump(self):
        network_id = uuid4()
        node_id = uuid4()
        instance_id = uuid4()
        central_node = uuid4()

        network = Network(
            networkId=network_id,
            networkName='Test Network',
            description='A test network for unit testing.',
            nodeIds=[node_id],
            visible=True,
            registered=True,
            instanceId=instance_id,
            centralNode=central_node,
        )

        network_dict = network.model_dump()

        assert network_dict == {
            'networkId': str(network_id),
            'networkName': 'Test Network',
            'description': 'A test network for unit testing.',
            'nodeIds': [str(node_id)],
            'visible': True,
            'registered': True,
            'instanceId': str(instance_id),
            'centralNode': str(central_node),
        }

    def test_model_dump_json(self):
        network_id = uuid4()
        node_id = uuid4()
        instance_id = uuid4()
        central_node = uuid4()

        network = Network(
            networkId=network_id,
            networkName='Test Network',
            description='A test network for unit testing.',
            nodeIds=[node_id],
            visible=True,
            registered=True,
            instanceId=instance_id,
            centralNode=central_node,
        )

        network_json = network.model_dump_json()

        expected_json = (
            f'{{"networkId":"{str(network_id)}",'
            f'"networkName":"Test Network",'
            f'"description":"A test network for unit testing.",'
            f'"nodeIds":["{str(node_id)}"],'
            f'"visible":true,'
            f'"registered":true,'
            f'"instanceId":"{str(instance_id)}",'
            f'"centralNode":"{str(central_node)}"}}'
        )

        assert network_json == expected_json
