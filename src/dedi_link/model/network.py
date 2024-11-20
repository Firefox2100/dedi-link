import uuid
from typing import Generic, TypeVar

from dedi_link.etc.exceptions import NetworkNotImplemented
from .base_model import BaseModel
from .data_index import DataIndex, DataIndexType
from .node import Node, NodeType


NetworkType = TypeVar('NetworkType', bound='Network')


class Network(BaseModel, Generic[DataIndexType, NodeType]):
    """
    A network that contains nodes which agreed to share data among each other.

    A network is a logical abstraction of a group of nodes that accepts (partially)
    others credentials and allows access to their data.
    """
    DATA_INDEX_CLASS = DataIndex
    NODE_CLASS = Node

    def __init__(self,
                 network_id: str,
                 network_name: str,
                 description: str = '',
                 node_ids: list[str] | None = None,
                 visible: bool = False,
                 instance_id: str = None,
                 ):
        self.network_id = network_id
        self.network_name = network_name
        self.description = description
        self.visible = visible
        self.instance_id = instance_id or str(uuid.uuid4())
        self.node_ids = node_ids or []

    def __eq__(self, other):
        if not isinstance(other, Network):
            return NotImplemented

        return all([
            self.network_id == other.network_id,
            self.network_name == other.network_name,
            self.description == other.description,
            self.visible == other.visible,
            self.node_ids == other.node_ids,
        ])

    def __hash__(self):
        return hash(
            (
                self.network_id,
                self.network_name,
                self.description,
                self.visible,
                tuple(self.node_ids),
            )
        )

    @classmethod
    def from_dict(cls, payload: dict[str, str | list[str] | bool | dict]) -> 'Network':
        if 'networkId' not in payload or not payload['networkId']:
            payload['networkId'] = str(uuid.uuid4())

        if 'instanceId' not in payload or not payload['instanceId']:
            payload['instanceId'] = str(uuid.uuid4())

        return cls(
            network_id=payload['networkId'],
            network_name=payload['networkName'],
            description=payload['description'],
            node_ids=payload.get('nodeIds', []),
            visible=payload['visible'],
            instance_id=payload['instanceId'],
        )

    def to_dict(self) -> dict:
        return {
            'networkId': self.network_id,
            'networkName': self.network_name,
            'description': self.description,
            'nodeIds': self.node_ids,
            'visible': self.visible,
            'instanceId': self.instance_id,
        }

    def to_dict_with_index(self) -> dict:
        """
        Convert the network object to a dictionary, with index included.

        :return: Dictionary
        """
        data_index = self.network_data_index

        payload = self.to_dict()

        payload['dataIndex'] = data_index.to_dict()

        return payload

    @property
    def nodes(self) -> list[NodeType]:
        """
        Get all nodes in the network.

        :return: List of nodes
        """
        raise NetworkNotImplemented('nodes property not implemented')

    @property
    def nodes_pending(self) -> list[NodeType]:
        """
        Get pending nodes in the network.

        These nodes are part of the network as they are accepted by other
        nodes, but are not approved (yet) by this one.

        :return: List of nodes
        """
        raise NetworkNotImplemented('nodes_pending property not implemented')

    @property
    def nodes_approved(self) -> list[NodeType]:
        """
        Get approved nodes in the network.

        :return: List of nodes
        """
        raise NetworkNotImplemented('nodes_approved property not implemented')

    @property
    def self_data_index(self) -> DataIndexType:
        """
        Get the data index of the instance itself for this network.

        :return: DataIndex object
        """
        raise NetworkNotImplemented('self_data_index property not implemented')

    @property
    def network_data_index(self) -> DataIndexType:
        """
        Get the data index of the network.

        This is the union of all data indices of the nodes in the network.

        :return: DataIndex object
        """
        data_index = self.self_data_index

        nodes = self.nodes_approved

        for node in nodes:
            data_index += node.data_index

        return data_index

    @property
    def private_key(self) -> str:
        """
        Get the network private key.

        :return: Private key in PEM string format
        """
        raise NetworkNotImplemented('private_key property not implemented')
