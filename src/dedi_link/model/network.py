import uuid
from typing import Generic, TypeVar

from dedi_link.etc.exceptions import NetworkNotImplementedException
from .base_model import BaseModel
from .data_index import DataIndex, DataIndexType
from .node import Node, NodeType


NetworkType = TypeVar('NetworkType', bound='Network')


class Network(BaseModel, Generic[DataIndexType, NodeType]):
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
        if 'networkID' not in payload or not payload['networkID']:
            payload['networkID'] = str(uuid.uuid4())

        if 'instanceID' not in payload or not payload['instanceID']:
            payload['instanceID'] = str(uuid.uuid4())

        return cls(
            network_id=payload['networkID'],
            network_name=payload['networkName'],
            description=payload['description'],
            node_ids=payload.get('nodeIDs', []),
            visible=payload['visible'],
            instance_id=payload['instanceID'],
        )

    def to_dict(self) -> dict:
        return {
            'networkID': self.network_id,
            'networkName': self.network_name,
            'description': self.description,
            'nodeIDs': self.node_ids,
            'visible': self.visible,
            'instanceID': self.instance_id,
        }

    def to_dict_with_index(self) -> dict:
        """
        Convert the network object to a dictionary, with extra attributes.
        :return: Dictionary
        """
        data_index = self.network_data_index

        payload = self.to_dict()

        payload['dataIndex'] = data_index.to_dict()

        return payload

    @property
    def nodes(self) -> list[NodeType]:
        raise NetworkNotImplementedException('nodes property not implemented')

    @property
    def nodes_pending(self) -> list[NodeType]:
        raise NetworkNotImplementedException('nodes_pending property not implemented')

    @property
    def nodes_approved(self) -> list[NodeType]:
        raise NetworkNotImplementedException('nodes_approved property not implemented')

    @property
    def self_data_index(self) -> DataIndexType:
        raise NetworkNotImplementedException('self_data_index property not implemented')

    @property
    def network_data_index(self) -> DataIndexType:
        data_index = self.self_data_index

        nodes = self.nodes_approved

        for node in nodes:
            data_index += node.data_index

        return data_index
