from dedi_link.model import Network as NetworkLib
from dedi_link.model import DataIndex, UserMapping

from .base_model import BaseModel
from .node import Node


class Network(NetworkLib[DataIndex, UserMapping, Node], BaseModel):
    NODE_CLASS = Node

    @property
    def nodes(self) -> list[Node]:
        approved_nodes = self.nodes_approved
        pending_nodes = self.nodes_pending

        return approved_nodes + pending_nodes

    @property
    def nodes_pending(self) -> list[Node]:
        nodes = []

        for node_id in self.node_ids:
            node = Node.load_pending(node_id)

            if node is not None:
                nodes.append(node)

        return nodes

    @property
    def nodes_approved(self) -> list[Node]:
        nodes = []

        for node_id in self.node_ids:
            node = Node.load(node_id)

            if node is not None:
                nodes.append(node)

        return nodes

    @property
    def self_data_index(self) -> DataIndex:
        """
        Get the data index of the instance itself for this network.

        :return: DataIndex object
        """
        nodes = self.nodes_approved

        data_index = DataIndex()

        for node in nodes:
            data_index += node.data_index

        return data_index

    @classmethod
    def load(cls, network_id: str) -> 'Network':
        network_dict = next(n for n in cls.db.networks if n['networkId'] == network_id)

        return cls.from_dict(network_dict)

    @classmethod
    def load_all(cls) -> list['Network']:
        networks = []

        for network_dict in cls.db.networks:
            networks.append(cls.from_dict(network_dict))

        return networks

    def store(self):
        with self.db.commit_lock:
            existing_network = next(
                (n for n in self.db.networks if n['networkId'] == self.network_id),
                None
            )

            if existing_network:
                self.db.networks.remove(existing_network)

            self.db.networks.append(self.to_dict())

    def update(self, payload: dict):
        with self.db.commit_lock:
            network_dict = next(n for n in self.db.networks if n['networkId'] == self.network_id)

            for key, value in payload.items():
                network_dict[key] = value

    def delete(self):
        with self.db.commit_lock:
            network_dict = next(n for n in self.db.networks if n['networkId'] == self.network_id)
            self.db.networks.remove(network_dict)
