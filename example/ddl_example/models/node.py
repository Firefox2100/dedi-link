from typing import Union
from dedi_link.model import Node as NodeLib
from dedi_link.model import DataIndex, UserMapping

from .base_model import BaseModel


class Node(NodeLib[DataIndex, UserMapping], BaseModel):
    @classmethod
    def load(cls, node_id: str) -> Union['Node', None]:
        node_dict = next((n for n in cls.db.nodes if n['nodeId'] == node_id), None)

        if node_dict is None:
            return None

        return cls.from_dict(node_dict)

    @classmethod
    def load_pending(cls, node_id: str) -> Union['Node', None]:
        node_dict = next((n for n in cls.db.pending_nodes if n['nodeId'] == node_id), None)

        if node_dict is None:
            return None

        return cls.from_dict(node_dict)

    @classmethod
    def load_all(cls) -> list['Node']:
        nodes = []

        for node_dict in cls.db.nodes:
            nodes.append(cls.from_dict(node_dict))

        for node_dict in cls.db.pending_nodes:
            nodes.append(cls.from_dict(node_dict))

        return nodes

    def store(self):
        with self.db.commit_lock:
            existing_node = next(
                (n for n in self.db.nodes if n['nodeId'] == self.node_id),
                None
            )

            if existing_node:
                self.db.nodes.remove(existing_node)

            self.db.nodes.append(self.to_dict())

    def update(self, payload: dict):
        with self.db.commit_lock:
            node_dict = next(n for n in self.db.nodes if n['nodeId'] == self.node_id)

            for key, value in payload.items():
                node_dict[key] = value

    def delete(self):
        with self.db.commit_lock:
            node_dict = next(n for n in self.db.nodes if n['nodeId'] == self.node_id)
            self.db.nodes.remove(node_dict)

    def get_user_key(self, user_id: str) -> str:
        """
        Get the user key for the given user ID

        This key is usually stored in KMS or similar service,
        and should not be held in memory for long. This is why
        it's not stored as a property of the Node object.

        :param user_id: The user ID to get the key for
        :return: The user key
        """
        raise NotImplementedError('get_user_key method not implemented')
